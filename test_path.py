from pathlib import Path

# 模拟dashboard.py的位置
dashboard_file = Path("apps/dashboard/src/industrial_dashboard/dashboard.py")
print("dashboard.py位置:", dashboard_file)

# 测试.parent次数
p1 = dashboard_file.parent
print("1个parent:", p1)

p2 = dashboard_file.parent.parent
print("2个parent:", p2)

p3 = dashboard_file.parent.parent.parent
print("3个parent:", p3)

p4 = dashboard_file.parent.parent.parent.parent
print("4个parent:", p4)

# 测试文件路径
print("\n测试automation-data路径:")
f3 = p3 / "automation-data" / "v17-complete-features.json"
print("3个parent:", f3, "| Exists:", f3.exists())

f2 = p2 / "automation-data" / "v17-complete-features.json"  
print("2个parent:", f2, "| Exists:", f2.exists())

