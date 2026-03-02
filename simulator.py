import pandas as pd
import threading
import time
from sqlalchemy import create_engine, text


class RealTimeSimulator:
    def __init__(self, csv_path="Healthcare_Transformed.csv"):
        self.df = pd.read_csv(csv_path)
        self.current_index = 0
        self.inserted_records = []
        self.running = False
        self.lock = threading.Lock()

        self.engine = create_engine(
            "mysql+mysqlconnector://root:Sathish3718@localhost:3306/healthcare_db"
        )
        self._init_table()

    def _init_table(self):
        with self.engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS healthcare_stream"))
            conn.commit()

    def _insert_row(self, row):
        row_df = pd.DataFrame([row])
        row_df.to_sql(
            name="healthcare_stream",
            con=self.engine,
            if_exists="append",
            index=False,
        )

    def start(self, interval=10):
        self.running = True
        self.thread = threading.Thread(
            target=self._run, args=(interval,), daemon=True
        )
        self.thread.start()

    def _run(self, interval):
        while self.running and self.current_index < len(self.df):
            row = self.df.iloc[self.current_index]
            self._insert_row(row)

            with self.lock:
                self.inserted_records.append(row.to_dict())
                self.current_index += 1

            time.sleep(interval)

        self.running = False

    def get_latest(self, n=1):
        with self.lock:
            return self.inserted_records[-n:]

    def get_all_inserted(self):
        with self.lock:
            return list(self.inserted_records)

    def get_count(self):
        with self.lock:
            return len(self.inserted_records)

    def get_total_rows(self):
        return len(self.df)

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False
