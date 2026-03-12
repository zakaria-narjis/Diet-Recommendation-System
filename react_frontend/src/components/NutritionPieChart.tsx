import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { NUTRITION_COLUMNS, type NutritionKey } from "@/types/recipe";

const COLORS = [
  "hsl(152, 45%, 28%)", "hsl(16, 70%, 58%)", "hsl(36, 60%, 55%)",
  "hsl(200, 50%, 50%)", "hsl(280, 40%, 55%)", "hsl(100, 40%, 45%)",
  "hsl(340, 50%, 55%)", "hsl(60, 50%, 50%)", "hsl(220, 50%, 55%)",
];

interface Props {
  nutritionData: Record<NutritionKey, number>;
}

export default function NutritionPieChart({ nutritionData }: Props) {
  const data = NUTRITION_COLUMNS.filter(c => c !== 'Calories').map((col) => ({
    name: col.replace('Content', ''),
    value: +(nutritionData[col] ?? 0).toFixed(1),
  }));

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={3}
            dataKey="value"
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: "hsl(0, 0%, 100%)",
              border: "1px solid hsl(40, 15%, 88%)",
              borderRadius: "8px",
              fontSize: "12px",
            }}
            formatter={(value: number, name: string) => [`${value}g`, name]}
          />
          <Legend wrapperStyle={{ fontSize: "12px" }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
