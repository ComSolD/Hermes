import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ComposedChart
} from "recharts";


const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div
        style={{
          backgroundColor: "#2c3f44",
          border: "1px solid #444",
          borderRadius: "6px",
          padding: "8px 12px",
          color: "#fff",
        }}
      >
        <p style={{ margin: 0 }}>{label}</p>
        <p style={{ margin: 0, color: "#cccccc" }}>
          Значение: {payload[0].value}
        </p>
      </div>
    );
  }

  return null;
};

export const GraphDisplay = ({ data }) => {
  // Преобразуем список значений в формат { name, value }
  const chartData = data.map((val, idx) => ({
    name: `Матч ${idx + 1}`,
    value: Number(val),
  }));

  return (
    <div style={{ width: "100%", height: 300, marginTop: "20px" }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#445b5f" />
          <XAxis
            dataKey="name"
            stroke="#ccc"
            tick={{ fontSize: 12 }}
            axisLine={{ stroke: "#ccc" }}
            tickLine={{ stroke: "#ccc" }}
          />
          <YAxis
            stroke="#ccc"
            tick={{ fontSize: 12 }}
            axisLine={{ stroke: "#ccc" }}
            tickLine={{ stroke: "#ccc" }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(255,255,255,0.1)" }} />
          <Bar dataKey="value" fill="#36c" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};


const CustomBoxPlot = ({ x, y, width, height, payload }) => {
  const { min, q1, median, q3, max } = payload;
  const pxPerUnit = height / (max - min || 1);

  const boxWidth = 200;
  const centerX = x + (width - boxWidth) / 2;
  const labelX = centerX + boxWidth + 16;

  const yMax = y;
  const yMin = y + (max - min) * pxPerUnit;
  const yQ1 = y + (max - q1) * pxPerUnit;
  const yQ3 = y + (max - q3) * pxPerUnit;
  const yMedian = y + (max - median) * pxPerUnit;

  const renderLabel = (label, value, posY, alignLeft = false) => (
    <text
      x={alignLeft ? centerX - 16 : labelX}
      y={posY}
      fontSize={13}
      fill="#e0e0e0" // светло-серый
      dominantBaseline="middle"
      fontWeight="500"
      textAnchor={alignLeft ? "end" : "start"}
    >
      {label}: {Number(value).toFixed(1)}
    </text>
  );

  return (
    <g>
      {/* Усы */}
      <line x1={centerX + boxWidth / 2} x2={centerX + boxWidth / 2} y1={yMax} y2={yQ3} stroke="#aaa" />
      <line x1={centerX + boxWidth / 2} x2={centerX + boxWidth / 2} y1={yQ1} y2={yMin} stroke="#aaa" />
      <line x1={centerX} x2={centerX + boxWidth} y1={yMax} y2={yMax} stroke="#aaa" />
      <line x1={centerX} x2={centerX + boxWidth} y1={yMin} y2={yMin} stroke="#aaa" />

      {/* Бокс */}
      <rect
        x={centerX}
        y={yQ3}
        width={boxWidth}
        height={yQ1 - yQ3}
        fill="#5561a2"
        fillOpacity={0.8}
        stroke="#ccd3ff"
        rx={4}
      />

      {/* Медиана */}
      <line
        x1={centerX}
        x2={centerX + boxWidth}
        y1={yMedian}
        y2={yMedian}
        stroke="#fff"
        strokeWidth={2}
      />

      {/* Подписи */}
      {renderLabel("Максимальное значение", max, yMax)}
      {renderLabel("Верхняя граница", q3, yQ3)}
      {renderLabel("Медиана", median, yMedian, true)}
      {renderLabel("Нижняя граница", q1, yQ1)}
      {renderLabel("Минимальное значение", min, yMin)}
    </g>
  );
};



export const BoxPlotChart = ({ data }) => {
  const formattedData = [{
    ...data,
    name: "BoxPlot",
    boxValue: 1
  }];

  return (
    <div style={{
      width: "100%",
      height: "100%",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
    }}>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart
          layout="vertical"
          data={formattedData}
        >
          <XAxis type="number" hide />
          <YAxis type="category" dataKey="name" hide />
          <Tooltip content={() => null} cursor={false} />
          <Bar
            dataKey="boxValue"
            barSize={400}
            shape={(props) => <CustomBoxPlot {...props} />}
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

