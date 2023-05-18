from flask import Flask,request, jsonify
from flask_cors import CORS
import pymysql
import pandas as pd

# 创建Flask实例
app = Flask(__name__)
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

# dbcon = pymysql.connect(
#   host="39.107.97.152",
#   user="root",
#   password="Ccbupt1234!",
#   db = "china_data",
#   port=3306,
#   charset='utf8mb4',
#   connect_timeout=10,
#  )

dbcon = pymysql.connect(
  host="127.0.0.1",
  user="root",
  password="123456",
  db = "china_data",
  port=3306,
  charset='utf8mb4',
  connect_timeout=10,
 )

# 设置路由，装饰器绑定触发函数
@app.route("/")
def data_provided_allcity():
    res=[]
    sql_2020 = "select * from china_data"
    sql_2021 = "select * from china_data_2021"
    data_2020 = pd.read_sql(sql_2020,dbcon)
    data_2021 = pd.read_sql(sql_2021,dbcon)
    data_provided_2020=data_2020[['城市','总分']]
    data_provided_2021=data_2021[['城市','总分']]
    data_provided_2020.columns = ['name','value']
    data_provided_2021.columns = ['name','value']
    res.append({"year":2020,"data":data_provided_2020.to_json(orient='records',force_ascii=False)})
    res.append({"year":2021,"data":data_provided_2021.to_json(orient='records',force_ascii=False)})
    return res

@app.route("/radar")
def data_provided_city():
    city_name = request.args.get("city_name")
    map={}
    city_value=['生态禀赋','文化资源','政策地位','经济规模','交通规模','创新能力','基本保障','生活水平','主流评价','教育服务','医疗服务','文化服务','主流媒体','网络接入','舆情干预','媒体影响','群体情绪','城市标签','就学吸引','就业吸引','旅游吸引','外资吸引','会展竞争']
    res_value=[]
    res_rank=[]
    for v in city_value:
        sql = "select "+v+" from china_data where 城市="+city_name
        #Mysql8.x
        sql_rank="WITH a AS(SELECT 城市,RANK( ) OVER (ORDER BY "+v+" DESC) city_rank FROM china_data) SELECT city_rank FROM a WHERE 城市="+city_name
        #Mysql5.x
        # sql_rank="SELECT aaa.rank from(select `城市`,`"+v+"`, @rk := @rk+1 as rank from china_data,(select @rk:=0)  a order by `"+v+"` desc ) as aaa where `城市` ="+city_name
        data = pd.read_sql(sql,dbcon)
        data_rank=pd.read_sql(sql_rank,dbcon)
        res_value.append(format(data.iloc[0, 0],'.2f'))
        res_rank.append(float(data_rank.iloc[0, 0]))
    res=[{'name':city_name[1:-1],'value':res_value,'rank':res_rank}]
    # print(res)
    return jsonify(res)

@app.route("/softpower")
def data_provided_index():
    data_index = request.args.get("data_index")
    # data_index=data_index[1:-1]
    all_index=['生态禀赋','文化资源','政策地位','经济规模','交通规模','创新能力','基本保障','生活水平','主流评价','教育服务','医疗服务','文化服务','主流媒体','网络接入','舆情干预','媒体影响','群体情绪','城市标签','就学吸引','就业吸引','旅游吸引','外资吸引','会展竞争']
    all_city=['石家庄','太原','呼和浩特','沈阳','长春','哈尔滨','南京','杭州','合肥','福州','南昌','郑州','武汉','长沙','广州','南宁','海口','成都','贵阳','昆明','拉萨','西安','兰州','西宁','银川','乌鲁木齐','深圳','大连','宁波','青岛','厦门','苏州']
    res=[]
    if data_index not in all_index:
        return jsonify(res)
    for city_name in all_city:
        city_name="\""+city_name+"\""
        sql = "select "+data_index+" from china_data where 城市="+city_name
        #Mysql8.x
        sql_rank="WITH a AS(SELECT 城市,RANK( ) OVER (ORDER BY "+data_index+" DESC) city_rank FROM china_data) SELECT city_rank FROM a WHERE 城市="+city_name
        #Mysql5.x
        # sql_rank="select aaa.rank from(select `城市`,`"+data_index+"`, @rk := @rk+1 as rank from china_data,(select @rk:=0)  a order by `"+data_index+"` desc ) as aaa where `城市` ="+city_name
        data = pd.read_sql(sql,dbcon)
        data_rank=pd.read_sql(sql_rank,dbcon)
        temp_data={'name':city_name[1:-1],'data':float(data.iloc[0, 0]),'rank':float(data_rank.iloc[0, 0])}
        res.append(temp_data)
    # print(res)
    return jsonify(res)

# @app.route("/scatter")
# def data_provided_scatter():
#     res=[]
#     year= request.args.get("year")
#     if year not in ['2020','2021']:
#         return res
#     sql= "select * from city_scatter_"+year
#     # sql_2021 = "select * from city_scatter_2021"
#     data = pd.read_sql(sql,dbcon)
#     # data_2021 = pd.read_sql(sql_2021,dbcon)
#     data_provided=data[['城市','支撑性得分','效应性得分']]
#     for d in data_provided:
#         res.append([data['城市'],data['支撑性得分']])
#     # print(data_provided)
#     # data_provided_2021=data_2021[['城市','支撑性得分','效应性得分']]
#     # data_provided_2020.columns = ['name','value']
#     # data_provided_2021.columns = ['name','value']
#     # res.append(data_provided.to_json(orient='records',force_ascii=False))
#     return res

if __name__ == "__main__":
    # debug=True 代码修改能运行时生效，app.run运行服务
    # host默认127.0.0.1 端口默认5000
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.run(host="0.0.0.0")