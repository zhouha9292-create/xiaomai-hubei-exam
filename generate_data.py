import pandas as pd
import json

df = pd.read_excel('/data/inputs/小麦课堂  -湖北成考.xlsx', header=None)
data = df.iloc[6:].copy()
data.columns = ['school', 'level', 'major', 'duration', 'tuition', 'total_tuition']
data = data.dropna(subset=['school', 'major'])

# 清洗
data['school'] = data['school'].astype(str).str.strip()
data['level'] = data['level'].astype(str).str.strip()
data['major'] = data['major'].astype(str).str.strip()
data['duration'] = pd.to_numeric(data['duration'], errors='coerce').fillna(2.5)
data['tuition'] = pd.to_numeric(data['tuition'], errors='coerce').fillna(0).astype(int)
data['total_tuition'] = pd.to_numeric(data['total_tuition'], errors='coerce').fillna(0)

# 添加城市映射
city_map = {
    '三峡大学': '宜昌', '武汉科技大学': '武汉', '湖北师范大学': '黄石',
    '湖北第二师范学院': '武汉', '武汉工程大学': '武汉', '湖北工业大学': '武汉',
    '湖北经济学院': '武汉', '黄冈科技职业学院': '黄冈', '长江大学': '荆州',
    '湖北中医药大学': '武汉', '三峡电力职业学院': '宜昌', '荆楚理工学院': '荆门',
    '湖北开放大学': '武汉', '黄冈职业技术学院': '黄冈', '武汉轻工大学': '武汉',
    '湖北理工学院': '黄石', '武汉中南财经政法大学': '武汉', '荆州理工职业学院': '荆州',
    '荆州职业技术学院': '荆州', '华中农业大学': '武汉', '湖北文理学院': '襄阳',
    '湖北汽车工业学院': '十堰', '武汉纺织大学': '武汉', '湖北科技学院': '咸宁',
    '黄冈师范学院': '黄冈'
}
data['city'] = data['school'].map(city_map).fillna('武汉')

records = data[['school','level','major','duration','tuition','total_tuition','city']].to_dict('records')
js = "const SCHOOL_DATA = " + json.dumps(records, ensure_ascii=False) + ";"

with open('/data/workspace/data.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f"✅ 共 {len(records)} 条数据已写入 data.js")
print(f"📊 学校数: {len(set(r['school'] for r in records))}")
print(f"📊 城市数: {len(set(r['city'] for r in records))}")
