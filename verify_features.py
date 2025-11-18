import requests
import json

resp = requests.get("http://localhost:8877/api/project_scan")
data = resp.json()
features = data.get('features', {})
impl = features.get('implemented', [])
part = features.get('partial', [])
conf = features.get('conflicts', [])

print("=" * 60)
print("功能清单验证结果")
print("=" * 60)
print(f"\n已实现功能: {len(impl)} 个")
print(f"部分实现: {len(part)} 个")
print(f"冲突问题: {len(conf)} 个")
print(f"\n总计: {len(impl)+len(part)} 个功能")
print("\n" + "=" * 60)

if len(impl) >= 108:
    print("✅ 成功！功能清单已恢复108个！")
    print("请刷新浏览器: http://localhost:8877")
    print("按 Ctrl+F5 强制刷新")
else:
    print(f"⚠️  仍然只有 {len(impl)} 个，需要进一步检查")
print("=" * 60)

