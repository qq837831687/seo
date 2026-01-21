#!/usr/bin/env python3
"""
合规检查工具 - 广告法 + 医疗合规
"""

import re
import sys
from typing import List, Tuple

class ComplianceChecker:
    def __init__(self):
        # 广告法绝对化用语
        self.absolute_terms = [
            r'最', r'最佳', r'最好', r'最优', r'最有效', r'最强',
            r'第一', r'极品', r'顶级', r'极致', r'终极',
            r'100%', r'完全', r'绝对', r'永久', r'永远',
            r'全部', r'全面', r'全方位', r'彻底',
            r'包治', r'根治', r'不复发', r'无副作用', r'零风险',
            r'保证', r'肯定', r'神效', r'奇效', r'特效',
            r'立竿见影', r'马上见效', r'一夜见效'
        ]

        # 医疗禁用词
        self.medical_terms = [
            r'治疗', r'治愈', r'疗效', r'医治', r'诊疗', r'诊断',
            r'代替药物', r'替代药物', r'不用吃药', r'可以停药',
            r'有效', r'显效', r'高效', r'速效', r'强效',
            r'能治\w+病', r'对\w+病有效', r'预防\w+病'
        ]

        # 建议替换词
        self.replacements = {
            '最有效': '很有效',
            '最佳': '优选',
            '最好': '很好',
            '第一': '首选',
            '100%': '大部分',
            '完全': '基本',
            '绝对': '基本',
            '包治': '改善',
            '根治': '改善',
            '治疗': '调理',
            '治愈': '恢复',
            '疗效': '效果',
            '排毒': '清理'
        }

    def check_article(self, content: str) -> Tuple[List[dict], str]:
        """检查文章合规性"""
        issues = []

        # 检查绝对化用语
        for term in self.absolute_terms:
            matches = re.finditer(term, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                context = self.get_context(content, match.start(), match.end())

                issues.append({
                    'type': 'absolute_term',
                    'severity': 'high',
                    'line': line_num,
                    'text': match.group(),
                    'context': context,
                    'suggestion': self.replacements.get(match.group(), '请修改')
                })

        # 检查医疗禁用词
        for term in self.medical_terms:
            matches = re.finditer(term, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                context = self.get_context(content, match.start(), match.end())

                issues.append({
                    'type': 'medical_term',
                    'severity': 'high',
                    'line': line_num,
                    'text': match.group(),
                    'context': context,
                    'suggestion': self.replacements.get(match.group(), '请修改')
                })

        # 生成修改后版本
        fixed_content = self.fix_issues(content, issues)

        return issues, fixed_content

    def get_context(self, content: str, start: int, end: int, context_chars: int = 50) -> str:
        """获取上下文"""
        context_start = max(0, start - context_chars)
        context_end = min(len(content), end + context_chars)
        return content[context_start:context_end]

    def fix_issues(self, content: str, issues: List[dict]) -> str:
        """自动修复问题"""
        fixed = content

        for issue in issues:
            old_text = issue['text']
            new_text = issue['suggestion']

            if new_text != '请修改':
                fixed = fixed.replace(old_text, new_text)

        return fixed

    def generate_report(self, issues: List[dict], fixed_content: str) -> str:
        """生成合规报告"""
        report = ["## ✅ 合规检查结果\n"]

        if not issues:
            report.append("**未发现合规问题** ✅\n")
        else:
            report.append(f"**发现问题**: {len(issues)} 个\n\n")
            report.append("### 问题列表\n\n")

            for i, issue in enumerate(issues, 1):
                severity_icon = "🔴" if issue['severity'] == 'high' else "⚠️"
                type_label = "广告法" if issue['type'] == 'absolute_term' else "医疗合规"

                report.append(f"{i}. {severity_icon} **{type_label}** (第{issue['line']}行)\n")
                report.append(f"   - 原文: `...{issue['context']}...`\n")
                report.append(f"   - 问题: `{issue['text']}`\n")
                report.append(f"   - 建议: 改为 `{issue['suggestion']}`\n\n")

            report.append("### 修改后版本\n\n")
            report.append("```markdown\n")
            report.append(fixed_content[:1000])  # 前1000字符预览
            if len(fixed_content) > 1000:
                report.append("\n\n... (内容过长，已截断)")
            report.append("\n```\n")

        # 添加免责声明检查
        if "免责声明" not in fixed_content and "仅供参考" not in fixed_content:
            report.append("\n### ⚠️ 缺少免责声明\n\n")
            report.append("建议添加:\n")
            report.append("```\n")
            report.append("---\n")
            report.append("*本文内容仅供健康科普参考，不能替代专业医疗诊断。如有身体不适，请及时就医。*\n")
            report.append("```\n")

        return "".join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python compliance_check.py <article_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    checker = ComplianceChecker()
    issues, fixed_content = checker.generate_report(content)

    print(checker.generate_report(issues, fixed_content))

    # 保存修改后版本
    if issues:
        output_path = file_path.replace('.md', '_fixed.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"\n修改后版本已保存到: {output_path}")

if __name__ == "__main__":
    main()
