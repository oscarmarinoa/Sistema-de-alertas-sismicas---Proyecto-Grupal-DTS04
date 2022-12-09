from google.cloud import bigquery
BIGQUERY_PROJECT_ID = 'sismos-project-3'  # poner el id del proyecto
BIGQUERY_DATASET_ID = 'data_sucia_g' # poner el id del dataset de BigQuery
BIGQUERY_TABLE_NAME = 'sismos' # poner un nombre cualquier para la tabla
PARTITION_FIELD = 'load_timestamp'  # no tocar
APPEND_DATA_ON_BIGQUERY = True  # cambiar a False en caso de querer que los nuevos datos reemplacen los viejos datos
def load_df_to_bigquery(project_id, dataset_id, table_name,
                        df, schema, append=False):
    try:
        print('Initializing GBQ Client..')
        client = bigquery.Client(project=project_id)
        # Get reference dataset
        dataset_ref = client.dataset(dataset_id)
        table_id = project_id+'.'+dataset_id+'.'+table_name
        try:
            # Check if table exists in reference dataset
            bq_table = client.get_table(table_id)
        except Exception:
            # Create table reference
            table_ref = dataset_ref.table(table_name)
            # Set table schema
            table = bigquery.Table(table_ref, schema=schema)
            # Create partition by date
            
           
            
            bq_table = client.get_table(table_id)
        # Load Job Config
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.json
        job_config.autodetect = True

        # Append or replace data
        if append is True:
            job_config.write_disposition = bigquery.\
                                           WriteDisposition.\
                                           WRITE_APPEND
        else:
            job_config.write_disposition = bigquery.\
                                           WriteDisposition.\
                                           WRITE_TRUNCATE

        job = client.load_table_from_dataframe(
            df,
            bq_table,
            job_config=job_config
        )
        job.result()
        return 200
    except Exception as e:
        print('[ERROR] {}'.format(e))
        return 400