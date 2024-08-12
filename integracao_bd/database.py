import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="10.230.80.14",
            database="db_dftrans_geo",
            user="ADALCSJ",
            password="Y3U8V2GmmR"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fetch_paradas_e_linhas(conn):
    query = """
    SELECT 
        p.cod_parada_dftrans,  
        p.seq_parada,  
        pr.geo_ponto_rede_pto,  
        geo.seq_linha, 
        geo.cod_linha, 
        geo.dsc_linha, 
        geo.dsc_sentido 
    FROM 
        geo.tab_paradas p  
    JOIN 
        geo.tab_pontos_rede pr  
        ON pr.seq_ponto_rede = p.seq_ponto_rede  
    JOIN 
        geo.tab_closest_point cp  
        ON cp.seq_parada = p.seq_parada  
    JOIN 
        geo.tab_linhas geo  
        ON ST_DWithin(geo.geo_linhas_lin, cp.geo_closest_point, 1)
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results
