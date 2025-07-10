# Gitauking-Crypto-ETL-Pipeline-with-Airflow
This project is a real-time ETL (Extract, Transform, Load) pipeline that collects live cryptocurrency prices using the CoinGecko API, transforms the data, and loads it into a PostgreSQL database.

It uses Apache Airflow to schedule and orchestrate the pipeline, allowing automated data collection for:

✅ Bitcoin (BTC)

✅ Ethereum (ETH)

✅ Solana (SOL)

✅ Dogecoin (DOGE)


🛠️ Tools & Technologies:
Apache Airflow 2

PostgreSQL + DBeaver

Python + psycopg2

CoinGecko API

Linux 
📁 Folder Structure
bash
Copy
Edit
airflow_crypto_etl/
├── dags/
│   └── crypto_etl_dag.py     # Main ETL DAG
├── venv/                     # Python virtual environment
├── logs/                     # Airflow logs
├── README.md
└── .gitignore
