import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { useAuth0 } from "@auth0/auth0-react";

const Linechart = () => {
  const [chartData, setChartData] = useState({
    options: {
      chart: {
        id: "temperature-evolution",
      },
      xaxis: {
        categories: [],
        title: { text: "Hora" },
      },
      yaxis: {
        title: { text: "Temperatura (°C)" },
      },
    },
    series: [
      {
        name: "Temperatura",
        data: [],
      },
    ],
  });
  const {
    user,
    isAuthenticated,
    isLoading,
    getAccessTokenSilently,
  } = useAuth0();

  useEffect(() => {
    const fetchData = async () => {
      if (!isAuthenticated) return;
      try {
        const sub = user.sub;
        const response = await fetch(`${import.meta.env.VITE_DDBB_API_IP}/db/reads/`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_SECRET_TOKEN}`,  // Enviar el token en el header
              'UserAuth': `${sub}`,
            },
          }
        );
        const data = await response.json();

        if (data.reads) {
          const sortedReads = data.reads.sort((a, b) => new Date(a.date) - new Date(b.date));
          const timestamps = sortedReads.map((read) => new Date(read.date).toLocaleTimeString());
          const temperatures = sortedReads.map((read) => read.temperature);

          setChartData({
            options: {
              chart: { id: "temperature-evolution" },
              xaxis: { categories: timestamps, title: { text: "Hora" } },
              yaxis: { title: { text: "Temperatura (°C)" } },
            },
            series: [{ name: "Temperatura", data: temperatures }],
          });
        }
      } catch (error) {
        console.error("Error al obtener los datos de temperatura:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="app">
      <div className="row">
        <div className="mixed-chart">
          <Chart options={chartData.options} series={chartData.series} type="line" width="600" />
        </div>
      </div>
    </div>
  );
};

export default Linechart;
