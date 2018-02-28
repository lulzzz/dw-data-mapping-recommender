from influxdb import DataFrameClient


class InfluxGateway(object):
    def get_values_dataframe(self, host='54.84.215.74', port=8086):
        """Instantiate the connection to the InfluxDB client."""
        user = 'menduz'
        password = 'shoki'
        dbname = 'apiled'

        client = DataFrameClient(host, port, user, password, dbname)
        requests = client.query("select * from requests")['requests']

        return requests
