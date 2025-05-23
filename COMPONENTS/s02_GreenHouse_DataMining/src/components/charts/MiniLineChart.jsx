import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { useAuth0 } from "@auth0/auth0-react";

// Mapeo de métricas a nombres y unidades
const METRIC_CONFIG = {
  temperature: { name: "Temperatura", unit: "°C" },
  water_temperature: { name: "Temp. Agua", unit: "°C" },
  humidity: { name: "Humedad", unit: "%" },
  tds: { name: "TDS", unit: "ppm" },
};

const MiniLineChart = ({
  metric = "temperature", // 'temperature' | 'water_temperature' | 'humidity' | 'tds'
  chartWidth = 200,
  chartHeight = 140,
}) => {
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
          // Ordenar por fecha
          const sortedReads = data.reads.sort(
            (a, b) => new Date(a.date) - new Date(b.date)
          );

          // Extraer timestamps y valores según la métrica
          const timestamps = sortedReads.map((read) =>
            new Date(read.date).toLocaleTimeString()
          );
          const values = sortedReads.map((read) => read[metric]);

          // Número de puntos para saber primer y último
          const n = timestamps.length;

          // Configuración del chart
          const { name, unit } = METRIC_CONFIG[metric] || {};
          setChartData({
            options: {
              chart: {
                id: `${metric}-evolution`,
                sparkline: { enabled: false },
                toolbar: { show: false },
              },
              stroke: { width: 2 },
              markers: { size: 0 },
              tooltip: {
                enabled: true,
                y: { formatter: (val) => `${val} ${unit}` },
              },
              xaxis: {
                categories: timestamps,
                labels: {
                  show: true,
                  style: {
                    colors: "#888",
                    fontSize: "8px",
                  },
                  // muestra solo primer y último tick
                  formatter: function (val, idx) {
                    return idx === 0 || idx === n - 1 ? val : "";
                  },
                },
                axisBorder: {
                  show: true,
                  color: "#DDD",
                },
                axisTicks: {
                  show: true,
                  color: "#DDD",
                  width: 1,
                },
              },
              yaxis: {
                show: true,
                min: Math.min(...values) * 0.98, // margen abajo
                max: Math.max(...values) * 1.02, // margen arriba
                labels: {
                  show: true,
                  style: {
                    colors: "#888",
                    fontSize: "8px",
                  },
                },
                axisBorder: {
                  show: true,
                  color: "#DDD",
                },
                axisTicks: {
                  show: true,
                  color: "#DDD",
                  width: 1,
                },
              },
              grid: {
                show: false, // sin cuadrícula para limpieza
              },
            },
            series: [{ name: name, data: values }],
          });
        }
      } catch (error) {
        console.error(`Error obteniendo datos de ${metric}:`, error);
      }
    };

    fetchData();
  }, [isAuthenticated, user, metric]);

  return (
    <div
      style={{
        width: chartWidth,
        height: chartHeight,
        overflow: "hidden",
      }}
    >
      <Chart
        options={chartData.options}
        series={chartData.series}
        type="line"
        width="100%"
        height="100%"
      />
    </div>
  );
};

export default MiniLineChart;
