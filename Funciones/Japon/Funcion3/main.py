from bigquery_uploader import load_df_to_bigquery
from sismos import extraerJapon
from schema import SCHEMA
def main(request):

    try:

        # PROJECT VARIABLES
        BIGQUERY_PROJECT_ID = 'sismos-project-3'  # poner el id del proyecto
        BIGQUERY_DATASET_ID = 'data_sucia_g' # poner el id del dataset de BigQuery
        BIGQUERY_TABLE_NAME = 'sismos' # poner un nombre cualquier para la tabla
        APPEND_DATA_ON_BIGQUERY = True

        # Request dolar data
        sismo_data = extraerJapon()

        # Check is the created dataframe is not empty
        if sismo_data  is None or len(sismo_data ) == 0:
            print('No content, table has 0 rows')
            return ('No content, table has 0 rows', 204)

        # Save on Google Big Query
        print("saving data into Google Big Query....")
        http_status = load_df_to_bigquery(
            project_id=BIGQUERY_PROJECT_ID,
            dataset_id=BIGQUERY_DATASET_ID,
            table_name=BIGQUERY_TABLE_NAME,
            df=sismo_data ,
            append=APPEND_DATA_ON_BIGQUERY
        )

        if http_status == 200:
            return ('Successful!', http_status)
        else:
            return ("Error. Please check the logging pannel", http_status)

    except Exception as e:
        error_message = "Error uploading data: {}".format(e)
        print('[ERROR] ' + error_message)
        return (error_message, '400')