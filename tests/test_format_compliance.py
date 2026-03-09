#!/usr/bin/env python3
"""
格式规范符合性测试

本测试验证LaTeX模板是否符合《江苏海洋大学2026届毕业实习与设计（论文）工作手册》规定的格式要求。

注意：工作手册只规定格式要求，不提供具体表格模板。
因此本测试验证：
1. 页面设置（纸张、边距）
2. 字体字号
3. 行距
4. 表格格式（三线表规范）
而不是对比Word XML中的具体表格结构。
"""

import re
from pathlib import Path

class FormatComplianceTest:
    """格式规范符合性测试类"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        
    def test_page_setup(self):
        """测试页面设置"""
        print("\n" + "="*60)
        print("测试1: 页面设置（A4纸张，2.5cm边距）")
        print("="*60)
        
        # 读取样式文件
        with open('styles/jouthesis.cls', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查geometry设置
        geometry_match = re.search(r'\\geometry\{([^}]+)\}', content, re.DOTALL)
        if not geometry_match:
            print("❌ 未找到geometry设置")
            self.failed += 1
            return False
            
        geo_params = geometry_match.group(1)
        
        # 验证A4纸张
        if 'a4paper' in geo_params:
            print("✅ 纸张: A4")
        else:
            print("❌ 纸张: 不是A4")
            self.failed += 1
            return False
            
        # 验证边距 (2.5cm)
        margins = {}
        for margin in ['top', 'bottom', 'left', 'right']:
            match = re.search(rf'{margin}=([0-9.]+)cm', geo_params)
            if match:
                margins[margin] = float(match.group(1))
        
        all_correct = True
        for margin, value in margins.items():
            if value == 2.5:
                print(f"✅ {margin}边距: {value}cm")
            else:
                print(f"❌ {margin}边距: {value}cm (要求2.5cm)")
                all_correct = False
        
        if all_correct:
            self.passed += 1
            return True
        else:
            self.failed += 1
            return False
    
    def test_line_spacing(self):
        """测试行距（1.25倍）"""
        print("\n" + "="*60)
        print("测试2: 行距（1.25倍）")
        print("="*60)
        
        with open('styles/jouthesis.cls', 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'\\linespread\{([0-9.]+)\}', content)
        if match:
            spacing = float(match.group(1))
            if spacing == 1.25:
                print(f"✅ 行距: {spacing}倍")
                self.passed += 1
                return True
            else:
                print(f"❌ 行距: {spacing}倍 (要求1.25倍)")
                self.failed += 1
                return False
        else:
            print("❌ 未找到行距设置")
            self.failed += 1
            return False
    
    def test_fonts(self):
        """测试字体字号"""
        print("\n" + "="*60)
        print("测试3: 字体字号")
        print("="*60)
        
        with open('styles/jouheadings.sty', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证章节标题字号
        tests = [
            (r'chapter=\{.*?format=\{\\JOUHeadingHei\\zihao\{-3\}', "一级标题", "小三号黑体"),
            (r'section=\{.*?format=\{\\JOUHeadingHei\\zihao\{-4\}', "二级标题", "小四号黑体"),
            (r'subsection=\{.*?format=\{\\JOUHeadingHei\\zihao\{-4\}', "三级标题", "小四号黑体"),
        ]
        
        all_passed = True
        for pattern, name, desc in tests:
            if re.search(pattern, content, re.DOTALL):
                print(f"✅ {name}: {desc}")
            else:
                print(f"❌ {name}: 未找到{desc}设置")
                all_passed = False
        
        if all_passed:
            self.passed += 1
            return True
        else:
            self.failed += 1
            return False
    
    def test_table_packages(self):
        """测试表格宏包（三线表支持）"""
        print("\n" + "="*60)
        print("测试4: 表格宏包（三线表规范）")
        print("="*60)
        
        with open('styles/jouthesis.cls', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_packages = {
            'booktabs': '三线表',
            'array': '表格增强',
            'multirow': '跨行单元格',
            'makecell': '单元格内换行',
        }
        
        all_passed = True
        for pkg, desc in required_packages.items():
            if f'RequirePackage{{{pkg}}}' in content:
                print(f"✅ {pkg}: {desc}")
            else:
                print(f"❌ {pkg}: 缺少{desc}支持")
                all_passed = False
        
        # 验证三线表参数
        if '\\heavyrulewidth' in content and '\\lightrulewidth' in content:
            print("✅ 三线表线宽参数已配置")
        else:
            print("❌ 三线表线宽参数未配置")
            all_passed = False
        
        if all_passed:
            self.passed += 1
            return True
        else:
            self.failed += 1
            return False
    
    def test_template_completeness(self):
        """测试模板完整性（17个模板）"""
        print("\n" + "="*60)
        print("测试5: 模板完整性（17个必需模板）")
        print("="*60)
        
        required_templates = {
            'forms/topic-selection.tex': '选题审题表',
            'forms/internship-registration.tex': '实习登记表',
            'forms/task-book-science.tex': '任务书（理工）',
            'forms/task-book-humanities.tex': '任务书（人文）',
            'forms/proposal-defense-record.tex': '开题答辩记录',
            'forms/midterm-check.tex': '中期检查表',
            'forms/defense-record.tex': '答辩记录',
            'reports/internship-diary.tex': '实习日记',
            'reports/internship-report.tex': '实习报告',
            'reports/proposal-science.tex': '开题报告（理工）',
            'reports/proposal-humanities.tex': '开题报告（人文）',
            'reports/excellent-thesis-abstract.tex': '校优摘要',
            'reports/translation.tex': '外文翻译',
            'evaluations/thesis-evaluation.tex': '论文评语',
            'evaluations/grading-science.tex': '评分表（理工）',
            'evaluations/grading-humanities.tex': '评分表（人文）',
        }
        
        all_exist = True
        for template, desc in required_templates.items():
            path = Path('templates') / template
            if path.exists():
                print(f"✅ {desc}: {template}")
            else:
                print(f"❌ {desc}: 缺失")
                all_exist = False
        
        if all_exist:
            print(f"\n✅ 所有16个配套模板完整")
            print(f"✅ 加上主模板(main.tex)，共17个模板")
            self.passed += 1
            return True
        else:
            self.failed += 1
            return False
    
    def test_logo_integration(self):
        """测试Logo集成"""
        print("\n" + "="*60)
        print("测试6: 学校视觉资源集成")
        print("="*60)
        
        # 检查logo文件
        logos = {
            'jou-logo-full.png': '封面主logo (1237×873px)',
            'jou-name-large.png': '大横版校名 (798×160px)',
            'jou-name-small.png': '小横版校名 (433×99px)',
            'jou-name-large-rgba.png': '透明背景版 (798×160px)',
            'jou-cover-header-clean.png': '论文封面页眉组合图',
        }
        
        all_exist = True
        for logo, desc in logos.items():
            path = Path('figures') / logo
            if path.exists():
                print(f"✅ {logo}: {desc}")
            else:
                print(f"❌ {logo}: 缺失")
                all_exist = False
        
        # 检查主模板中logo使用
        with open('styles/jouthesis.cls', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '\\newcommand{\\JOUCoverHeader}{figures/jou-cover-header-clean.png}' in content:
            print("✅ 封面页眉资源已配置")
        else:
            print("❌ 封面页眉资源未配置")
            all_exist = False
        
        if all_exist:
            self.passed += 1
            return True
        else:
            self.failed += 1
            return False

    def test_abstract_font_rules(self):
        """测试摘要页字体规则"""
        print("\n" + "="*60)
        print("测试7: 摘要页字体规则")
        print("="*60)

        with open('styles/jouthesis.cls', 'r', encoding='utf-8') as f:
            thesis_cls = f.read()

        all_passed = True

        if '\\RequirePackage[preferwps]{styles/joufonts}' in thesis_cls:
            print("✅ 主模板默认启用 preferwps 字体路由")
        else:
            print("❌ 主模板未启用 preferwps 字体路由")
            all_passed = False

        if r'{\JOUAbstractHei\bfseries\zihao{4}\@title}' in thesis_cls:
            print("✅ 中文摘要题名使用四号黑体")
        else:
            print("❌ 中文摘要题名不是四号黑体")
            all_passed = False

        if r'{\noindent{\JOUAbstractHei\bfseries\zihao{-4}摘\hspace{1em}要：}\zihao{-4}\songti}' in thesis_cls:
            print("✅ 中文摘要标签与正文字体分离正确")
        else:
            print("❌ 中文摘要标签/正文字体规则不符合预期")
            all_passed = False

        if all_passed:
            self.passed += 1
            return True
        else:
            self.failed += 1
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "🧪 "*30)
        print("江苏海洋大学LaTeX模板 - 格式规范符合性测试")
        print("🧪 "*30)
        
        self.test_page_setup()
        self.test_line_spacing()
        self.test_fonts()
        self.test_table_packages()
        self.test_template_completeness()
        self.test_logo_integration()
        self.test_abstract_font_rules()
        
        # 总结
        print("\n" + "="*60)
        print("测试总结")
        print("="*60)
        print(f"✅ 通过: {self.passed}/7")
        print(f"❌ 失败: {self.failed}/7")
        
        if self.failed == 0:
            print("\n🎉 所有测试通过！模板完全符合格式规范！")
            return 0
        else:
            print(f"\n⚠️  存在 {self.failed} 项不符合，需要修正")
            return 1

if __name__ == "__main__":
    tester = FormatComplianceTest()
    exit(tester.run_all_tests())
