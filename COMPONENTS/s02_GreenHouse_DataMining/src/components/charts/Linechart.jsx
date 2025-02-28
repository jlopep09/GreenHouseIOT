import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";

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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8002/db/reads/");
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
