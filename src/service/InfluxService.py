from src.service.gateway.InfluxGateway import InfluxGateway


class InfluxService(object):
    def get_values_from_domain(self, domain):
        influx_gateway = InfluxGateway()
        df_values = influx_gateway.get_values_dataframe()
        df_values_from_domain = df_values.loc[df_values['domain'] == domain]

        return df_values_from_domain
