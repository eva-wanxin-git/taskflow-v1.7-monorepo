#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试运行器 - INTEGRATE-007

运行所有E2E和集成测试，生成完整报告

使用方法:
    python tests/run_integration_tests.py              # 运行所有测试
    python tests/run_integration_tests.py --suite e2e  # 仅运行E2E测试
    python tests/run_integration_tests.py --report      # 生成测试报告
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"
REPORTS_DIR = PROJECT_ROOT / "tests" / "reports"

# 创建报告目录
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# 颜色输出
# ============================================================================

class Colors:
    """ANSI颜色代码"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


# ============================================================================
# 测试运行器
# ============================================================================

class IntegrationTestRunner:
    """集成测试运行器"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def run_e2e_tests(self):
        """运行E2E测试"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}运行E2E测试{Colors.END}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        test_files = [
            "tests/e2e/test_architect_api_e2e.py",
            "tests/e2e/test_complete_workflow_e2e.py"
        ]
        
        for test_file in test_files:
            test_path = PROJECT_ROOT / test_file
            
            if test_path.exists():
                print(f"{Colors.BLUE}▶{Colors.END} 运行 {test_file}")
                
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True
                )
                
                result_data = {
                    "test_file": test_file,
                    "status_code": result.returncode,
                    "passed": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
                self.results.append(result_data)
                
                if result.returncode == 0:
                    print(f"{Colors.GREEN}✓{Colors.END} {test_file} 通过\n")
                else:
                    print(f"{Colors.RED}✗{Colors.END} {test_file} 失败\n")
            else:
                print(f"{Colors.YELLOW}⚠{Colors.END} {test_file} 不存在\n")
    
    def run_integration_tests(self):
        """运行集成测试"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}运行集成测试{Colors.END}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        test_files = [
            "tests/integration/test_all_features.py",
            "tests/integration/test_system_integration_e2e.py"
        ]
        
        for test_file in test_files:
            test_path = PROJECT_ROOT / test_file
            
            if test_path.exists():
                print(f"{Colors.BLUE}▶{Colors.END} 运行 {test_file}")
                
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True
                )
                
                result_data = {
                    "test_file": test_file,
                    "status_code": result.returncode,
                    "passed": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
                self.results.append(result_data)
                
                if result.returncode == 0:
                    print(f"{Colors.GREEN}✓{Colors.END} {test_file} 通过\n")
                else:
                    print(f"{Colors.RED}✗{Colors.END} {test_file} 失败\n")
            else:
                print(f"{Colors.YELLOW}⚠{Colors.END} {test_file} 不存在\n")
    
    def run_all_tests(self):
        """运行所有测试"""
        self.start_time = datetime.now()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("="*70)
        print("🎯 任务所·Flow v1.7 - 集成测试套件")
        print("任务ID: INTEGRATE-007")
        print(f"开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print(f"{Colors.END}")
        
        # 运行测试
        self.run_e2e_tests()
        self.run_integration_tests()
        
        self.end_time = datetime.now()
        
        # 生成报告
        self.print_summary()
        self.generate_report()
    
    def print_summary(self):
        """打印测试总结"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}测试总结{Colors.END}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        
        # 统计
        print(f"总计: {total} 个测试")
        print(f"通过: {Colors.GREEN}{passed}{Colors.END}")
        print(f"失败: {Colors.RED}{failed}{Colors.END}")
        print(f"通过率: {Colors.BOLD}{passed/total*100:.1f}%{Colors.END}")
        
        # 耗时
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"耗时: {duration:.2f}秒")
        
        # 详细结果
        print(f"\n{Colors.BOLD}详细结果:{Colors.END}\n")
        
        for result in self.results:
            status_icon = f"{Colors.GREEN}✓{Colors.END}" if result["passed"] else f"{Colors.RED}✗{Colors.END}"
            print(f"{status_icon} {result['test_file']}")
        
        # 最终结论
        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
        
        if passed == total:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ 所有测试通过！可以部署到生产环境{Colors.END}")
        elif passed >= total * 0.8:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠ 大部分测试通过，建议review后再部署{Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ 测试失败过多，需要修复{Colors.END}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    def generate_report(self):
        """生成JSON报告"""
        report = {
            "test_suite": "INTEGRATE-007: E2E集成测试",
            "timestamp": datetime.now().isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": (self.end_time - self.start_time).total_seconds(),
            "summary": {
                "total": len(self.results),
                "passed": sum(1 for r in self.results if r["passed"]),
                "failed": sum(1 for r in self.results if not r["passed"]),
                "pass_rate": f"{sum(1 for r in self.results if r['passed']) / len(self.results) * 100:.1f}%"
            },
            "results": [
                {
                    "test_file": r["test_file"],
                    "status": "PASS" if r["passed"] else "FAIL",
                    "status_code": r["status_code"]
                }
                for r in self.results
            ]
        }
        
        # 保存JSON报告
        report_file = REPORTS_DIR / f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 测试报告已保存: {report_file}\n")
        
        return report


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="任务所·Flow v1.7 集成测试运行器"
    )
    
    parser.add_argument(
        "--suite",
        choices=["all", "e2e", "integration"],
        default="all",
        help="运行指定的测试套件 (默认: 全部)"
    )
    
    parser.add_argument(
        "--report",
        action="store_true",
        help="仅生成报告，不运行测试"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="详细输出"
    )
    
    args = parser.parse_args()
    
    runner = IntegrationTestRunner()
    
    if args.report:
        print(f"报告目录: {REPORTS_DIR}")
    else:
        if args.suite in ["all", "e2e"]:
            runner.run_e2e_tests()
        
        if args.suite in ["all", "integration"]:
            runner.run_integration_tests()
        
        runner.print_summary()
        runner.generate_report()
    
    # 返回状态码
    if runner.results:
        passed = sum(1 for r in runner.results if r["passed"])
        return 0 if passed == len(runner.results) else 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
