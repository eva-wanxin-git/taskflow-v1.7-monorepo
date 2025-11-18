/**
 * Service Worker - 版本控制和缓存管理
 * 
 * 功能：
 * 1. 版本控制 - 检测版本更新并自动刷新
 * 2. 智能缓存 - 缓存静态资源，但HTML始终从网络获取
 * 3. 缓存清除 - 版本更新时清除旧缓存
 */

const CACHE_PREFIX = 'taskflow-dashboard';
let CACHE_VERSION = 'v1'; // 默认版本，将从服务器获取

// 需要缓存的静态资源
const STATIC_CACHE_URLS = [
    '/static/ui/',
    '/static/ux/'
];

// 不缓存的路径（HTML和API）
const NO_CACHE_PATTERNS = [
    /^\/$/,              // 首页
    /^\/api\//,          // 所有API
    /\.html$/            // HTML文件
];

/**
 * 检查URL是否应该被缓存
 */
function shouldCache(url) {
    const urlPath = new URL(url).pathname;
    
    // 检查是否匹配不缓存的模式
    for (const pattern of NO_CACHE_PATTERNS) {
        if (pattern.test(urlPath)) {
            return false;
        }
    }
    
    // 检查是否是静态资源
    return STATIC_CACHE_URLS.some(prefix => urlPath.startsWith(prefix));
}

/**
 * 获取缓存名称
 */
function getCacheName() {
    return `${CACHE_PREFIX}-${CACHE_VERSION}`;
}

/**
 * 从服务器获取最新版本号
 */
async function fetchLatestVersion() {
    try {
        const response = await fetch('/api/cache/version');
        const data = await response.json();
        if (data.success && data.data.current_version) {
            return data.data.current_version;
        }
    } catch (error) {
        console.warn('[SW] 获取版本号失败:', error);
    }
    return CACHE_VERSION;
}

/**
 * 清除旧缓存
 */
async function clearOldCaches() {
    const currentCache = getCacheName();
    const cacheNames = await caches.keys();
    
    const deletePromises = cacheNames
        .filter(name => name.startsWith(CACHE_PREFIX) && name !== currentCache)
        .map(name => {
            console.log('[SW] 删除旧缓存:', name);
            return caches.delete(name);
        });
    
    await Promise.all(deletePromises);
}

// Service Worker 安装事件
self.addEventListener('install', event => {
    console.log('[SW] 安装中...');
    
    // 立即激活新的Service Worker
    self.skipWaiting();
    
    event.waitUntil(
        fetchLatestVersion().then(version => {
            CACHE_VERSION = version;
            console.log('[SW] 当前版本:', CACHE_VERSION);
        })
    );
});

// Service Worker 激活事件
self.addEventListener('activate', event => {
    console.log('[SW] 激活中...');
    
    event.waitUntil(
        clearOldCaches().then(() => {
            console.log('[SW] 旧缓存已清除');
            // 立即控制所有页面
            return self.clients.claim();
        })
    );
});

// 拦截网络请求
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = request.url;
    
    // 对于不需要缓存的请求，直接从网络获取
    if (!shouldCache(url)) {
        event.respondWith(
            fetch(request).catch(error => {
                console.error('[SW] 网络请求失败:', url, error);
                return new Response('网络错误', { status: 503 });
            })
        );
        return;
    }
    
    // 对于静态资源，使用缓存优先策略
    event.respondWith(
        caches.match(request).then(cachedResponse => {
            if (cachedResponse) {
                console.log('[SW] 从缓存返回:', url);
                return cachedResponse;
            }
            
            // 缓存中没有，从网络获取并缓存
            return fetch(request).then(response => {
                // 检查响应是否有效
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }
                
                // 克隆响应（因为响应只能使用一次）
                const responseToCache = response.clone();
                
                caches.open(getCacheName()).then(cache => {
                    cache.put(request, responseToCache);
                    console.log('[SW] 已缓存:', url);
                });
                
                return response;
            }).catch(error => {
                console.error('[SW] 网络请求失败:', url, error);
                return new Response('网络错误', { status: 503 });
            });
        })
    );
});

// 监听消息（用于手动清除缓存）
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        console.log('[SW] 收到清除缓存命令');
        event.waitUntil(
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(name => name.startsWith(CACHE_PREFIX))
                        .map(name => caches.delete(name))
                );
            }).then(() => {
                console.log('[SW] 所有缓存已清除');
                // 通知客户端刷新
                self.clients.matchAll().then(clients => {
                    clients.forEach(client => {
                        client.postMessage({
                            type: 'CACHE_CLEARED',
                            message: '缓存已清除，即将刷新页面'
                        });
                    });
                });
            })
        );
    }
    
    if (event.data && event.data.type === 'CHECK_VERSION') {
        console.log('[SW] 检查版本更新');
        event.waitUntil(
            fetchLatestVersion().then(latestVersion => {
                if (latestVersion !== CACHE_VERSION) {
                    console.log('[SW] 发现新版本:', latestVersion, '当前版本:', CACHE_VERSION);
                    CACHE_VERSION = latestVersion;
                    
                    // 通知客户端有新版本
                    self.clients.matchAll().then(clients => {
                        clients.forEach(client => {
                            client.postMessage({
                                type: 'NEW_VERSION',
                                oldVersion: CACHE_VERSION,
                                newVersion: latestVersion,
                                message: '发现新版本，建议刷新页面'
                            });
                        });
                    });
                    
                    // 清除旧缓存
                    return clearOldCaches();
                }
            })
        );
    }
});

console.log('[SW] Service Worker 已加载');

