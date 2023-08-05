"""
计算公司员工工资
"""
company = "菠菜理财"
def yearSalary(monthSalary):
    """根据月薪计算员工年薪计算公式：monthSalary*12"""
    return monthSalary*12

def daySalary(monrhSalary):
    """根据月薪，计算员工日薪，计算公式：monthSalary/22.5"""
    return monrhSalary/22.5

if __name__=="__main__":
    print(yearSalary(10000))