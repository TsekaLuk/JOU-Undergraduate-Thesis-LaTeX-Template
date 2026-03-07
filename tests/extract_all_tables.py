#!/usr/bin/env python3
"""
从Word XML完整提取所有表格的精确结构

提取内容：
1. 每个表格的网格列定义 (w:tblGrid → w:gridCol)
2. 每行的单元格结构 (w:tc, w:gridSpan, w:tcW)
3. 每个单元格的文本内容（用于标识表格类型）
4. 行高、合并等信息
"""

import xml.etree.ElementTree as ET
import json
import os

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
}

def get_text(element):
    """递归提取元素中的所有文本"""
    texts = []
    for t in element.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
        if t.text:
            texts.append(t.text)
    return ''.join(texts).strip()

def extract_cell_info(tc):
    """提取单元格信息"""
    cell = {}

    # 获取单元格属性
    tcPr = tc.find('w:tcPr', NS)
    if tcPr is not None:
        # 宽度
        tcW = tcPr.find('w:tcW', NS)
        if tcW is not None:
            w_val = tcW.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
            w_type = tcW.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
            if w_val:
                cell['width_dxa'] = int(w_val)
                cell['width_cm'] = round(int(w_val) / 567, 2)
            if w_type:
                cell['width_type'] = w_type

        # 跨列
        gridSpan = tcPr.find('w:gridSpan', NS)
        if gridSpan is not None:
            val = gridSpan.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            if val:
                cell['gridSpan'] = int(val)

        # 垂直合并
        vMerge = tcPr.find('w:vMerge', NS)
        if vMerge is not None:
            val = vMerge.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            cell['vMerge'] = val if val else 'continue'

    # 获取文本
    cell['text'] = get_text(tc)

    return cell

def extract_table(tbl, table_index):
    """提取单个表格的完整结构"""
    table = {
        'index': table_index,
        'grid': [],
        'grid_cm': [],
        'total_width_dxa': 0,
        'total_width_cm': 0,
        'rows': [],
        'first_texts': [],  # 用于标识表格
    }

    # 提取网格定义
    tblGrid = tbl.find('w:tblGrid', NS)
    if tblGrid is not None:
        for gridCol in tblGrid.findall('w:gridCol', NS):
            w = gridCol.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
            if w:
                dxa = int(w)
                table['grid'].append(dxa)
                table['grid_cm'].append(round(dxa / 567, 2))

    table['total_width_dxa'] = sum(table['grid'])
    table['total_width_cm'] = round(sum(table['grid']) / 567, 2)
    table['num_grid_cols'] = len(table['grid'])

    # 提取表格属性
    tblPr = tbl.find('w:tblPr', NS)
    if tblPr is not None:
        tblW = tblPr.find('w:tblW', NS)
        if tblW is not None:
            w_val = tblW.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
            if w_val:
                table['declared_width_dxa'] = int(w_val)

    # 提取每行
    for row_idx, tr in enumerate(tbl.findall('w:tr', NS)):
        row = {
            'index': row_idx,
            'cells': [],
            'height_dxa': None,
        }

        # 行属性
        trPr = tr.find('w:trPr', NS)
        if trPr is not None:
            trHeight = trPr.find('w:trHeight', NS)
            if trHeight is not None:
                h = trHeight.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                if h:
                    row['height_dxa'] = int(h)
                    row['height_cm'] = round(int(h) / 567, 2)

        # 提取单元格
        for tc in tr.findall('w:tc', NS):
            cell = extract_cell_info(tc)
            row['cells'].append(cell)

        table['rows'].append(row)

    # 收集前几行文本用于标识
    for row in table['rows'][:3]:
        for cell in row['cells']:
            if cell.get('text'):
                table['first_texts'].append(cell['text'])

    table['num_rows'] = len(table['rows'])

    return table

def identify_table(table):
    """根据内容标识表格类型"""
    texts = ' '.join(table['first_texts'])

    # 匹配规则
    if '目' in texts and '录' in texts and '页码' in texts:
        return '目录索引表'
    elif '选题审题表' in texts or ('申报课题名称' in texts):
        return '选题审题表'
    elif '实习登记表' in texts or ('实习单位' in texts and '实习内容' in texts):
        return '实习登记表'
    elif '任务书' in texts and ('理工' in texts or '农医' in texts):
        return '任务书（理工农医类）'
    elif '任务书' in texts and '人文' in texts:
        return '任务书（人文经管类）'
    elif '开题报告' in texts and ('理工' in texts or '农医' in texts):
        return '开题报告（理工农医类）'
    elif '开题报告' in texts and '人文' in texts:
        return '开题报告（人文经管类）'
    elif '开题答辩' in texts or '答辩委员' in texts:
        return '开题答辩记录'
    elif '中期检查' in texts:
        return '中期检查表'
    elif '答辩记录' in texts or ('答辩' in texts and '记录' in texts):
        return '答辩记录'
    elif '实习日记' in texts or ('日期' in texts and '实习内容' in texts):
        return '实习日记'
    elif '实习报告' in texts:
        return '实习报告'
    elif '外文翻译' in texts or '翻译' in texts:
        return '外文翻译'
    elif '评语' in texts or '论文评语' in texts:
        return '论文评语'
    elif '评分' in texts and ('理工' in texts or '农医' in texts):
        return '评分表（理工农医类）'
    elif '评分' in texts and '人文' in texts:
        return '评分表（人文经管类）'
    elif '成绩' in texts and '评定' in texts:
        return '成绩评定表'
    elif '学生姓名' in texts and '学号' in texts:
        return '表头信息表'
    elif '主要内容' in texts or '要求' in texts:
        return '内容要求表'

    return f'未识别表格_{table["index"]}'

def main():
    xml_path = os.path.join(os.path.dirname(__file__),
                            '..', 'references', 'unpacked', 'word', 'document.xml')

    print("=" * 80)
    print("Word XML 完整表格结构提取")
    print("=" * 80)

    tree = ET.parse(xml_path)
    root = tree.getroot()

    tables = root.findall('.//w:tbl', NS)
    print(f"\n找到 {len(tables)} 个表格\n")

    all_tables = []

    for i, tbl in enumerate(tables):
        table = extract_table(tbl, i)
        table['identified_as'] = identify_table(table)
        all_tables.append(table)

        # 打印摘要
        print(f"\n{'='*70}")
        print(f"表格 {i}: {table['identified_as']}")
        print(f"{'='*70}")
        print(f"  网格列数: {table['num_grid_cols']}")
        print(f"  网格列宽(DXA): {table['grid']}")
        print(f"  网格列宽(cm):  {table['grid_cm']}")
        print(f"  总宽(cm): {table['total_width_cm']}")
        print(f"  行数: {table['num_rows']}")
        print(f"  首行文本: {table['first_texts'][:5]}")

        # 打印每行结构
        for row in table['rows'][:5]:  # 只显示前5行
            cells_desc = []
            for cell in row['cells']:
                span = cell.get('gridSpan', 1)
                w = cell.get('width_cm', '?')
                text = cell.get('text', '')[:15]
                if span > 1:
                    cells_desc.append(f"[span={span},w={w}cm]{text}")
                else:
                    cells_desc.append(f"[w={w}cm]{text}")
            print(f"  行{row['index']}: {' | '.join(cells_desc)}")

        if table['num_rows'] > 5:
            print(f"  ... (还有 {table['num_rows'] - 5} 行)")

    # 保存完整结构
    output_path = os.path.join(os.path.dirname(__file__), 'all_table_structures.json')

    # 简化输出（去掉过长的文本）
    output = []
    for t in all_tables:
        out_table = {
            'index': t['index'],
            'identified_as': t['identified_as'],
            'num_grid_cols': t['num_grid_cols'],
            'grid_dxa': t['grid'],
            'grid_cm': t['grid_cm'],
            'total_width_cm': t['total_width_cm'],
            'num_rows': t['num_rows'],
            'rows': []
        }
        for row in t['rows']:
            out_row = {
                'index': row['index'],
                'height_cm': row.get('height_cm'),
                'cells': []
            }
            for cell in row['cells']:
                out_cell = {
                    'width_cm': cell.get('width_cm'),
                    'width_dxa': cell.get('width_dxa'),
                    'gridSpan': cell.get('gridSpan', 1),
                    'text': cell.get('text', '')[:50],
                }
                if 'vMerge' in cell:
                    out_cell['vMerge'] = cell['vMerge']
                out_row['cells'].append(out_cell)
            out_table['rows'].append(out_row)
        output.append(out_table)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n\n完整结构已保存到: {output_path}")

    # 打印模板映射建议
    print("\n" + "=" * 80)
    print("模板映射建议")
    print("=" * 80)

    template_mapping = {}
    for t in all_tables:
        name = t['identified_as']
        if name not in template_mapping and '未识别' not in name and '目录' not in name:
            template_mapping[name] = {
                'table_index': t['index'],
                'grid_cm': t['grid_cm'],
                'total_cm': t['total_width_cm'],
                'num_rows': t['num_rows'],
            }

    for name, info in template_mapping.items():
        grid_str = ' + '.join([f"{w}cm" for w in info['grid_cm']])
        print(f"\n  {name}:")
        print(f"    表格索引: {info['table_index']}")
        print(f"    网格: {grid_str} = {info['total_cm']}cm")
        print(f"    行数: {info['num_rows']}")

if __name__ == '__main__':
    main()
