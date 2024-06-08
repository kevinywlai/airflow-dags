from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'spring_batch_trigger',
    default_args=default_args,
    description='Trigger Spring Batch Job',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    trigger_spring_batch = KubernetesPodOperator(
        namespace='spring-batch',
        image='your-docker-repo/your-spring-batch-app:latest',
        cmds=["java", "-jar", "/app/your-spring-batch-app.jar"],
        name='spring-batch-job',
        task_id='trigger_spring_batch',
        is_delete_operator_pod=True,
        in_cluster=True,
        get_logs=True,
    )

    trigger_spring_batch
