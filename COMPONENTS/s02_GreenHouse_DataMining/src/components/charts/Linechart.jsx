// Linechart.jsx
import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { useAuth0 } from "@auth0/auth0-react";

// Mismo mapeo de métricas que en MiniLineChart
const METRIC_CONFIG = {
  temperature: { name: "Temperatura", unit: "°C" },
  water_temperature: { name: "Temp. Agua", unit: "°C" },
  humidity: { name: "Humedad", unit: "%" },
  tds: { name: "TDS", unit: "ppm" },
};

const Linechart = ({ chartWidth = "100%", metric = "temperature" }) => {
  const [chartData, setChartData] = useState({ options: {}, series: [] });
  const { user, isAuthenticated } = useAuth0();

  useEffect(() => {
    const fetchData = async () => {
      if (!isAuthenticated) return;
      try {
        const sub = user.sub;
        const response = await fetch(
          `${import.meta.env.VITE_DDBB_API_IP}/db/reads/`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,
              UserAuth: `${sub}`,
            },
          }
        );
        const data = await response.json();

        if (data.reads) {
          const sortedReads = data.reads.sort(
            (a, b) => new Date(a.date) - new Date(b.date)
          );
          const timestamps = sortedReads.map((read) =>
            new Date(read.date).toLocaleTimeString()
          );
          const values = sortedReads.map((read) => read[metric]);

          const { name, unit } = METRIC_CONFIG[metric] || {};

          setChartData({
            options: {
              chart: { id: `${metric}-linechart` },
              xaxis: { categories: timestamps, title: { text: "Hora" } },
              yaxis: { title: { text: `${name} (${unit})` } },
              tooltip: {
                y: { formatter: (val) => `${val} ${unit}` },
              },
            },
            series: [{ name: name, data: values }],
          });
        }
      } catch (error) {
        console.error(`Error al obtener datos de ${metric}:`, error);
      }
    };

    fetchData();
  }, [isAuthenticated, user, metric]);

  return (
    <div className="app">
      <div className="row">
        <div className="mixed-chart">
          <Chart
            options={chartData.options}
            series={chartData.series}
            type="line"
            width={chartWidth}
          />
        </div>
      </div>
    </div>
  );
};

export default Linechart;
