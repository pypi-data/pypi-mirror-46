from lmf.dbv2 import db_query
def get_quyus(sheng):
    conp=["gpadmin",'since2015',"192.168.4.179","base_db","v"]
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='gg_html' and schemaname='v'  order by partitionname
    """
    df=db_query(sql,dbtype="postgresql",conp=conp)
    arr=df.loc[df['partitionname'].str.contains("^%s_"%sheng),'partitionname'].values.tolist()
    return arr




