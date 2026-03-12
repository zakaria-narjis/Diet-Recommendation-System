import { Activity } from "lucide-react";

interface Props {
  bmi: number;
}

function getBMICategory(bmi: number) {
  if (bmi < 18.5) return { label: "Underweight", color: "text-accent" };
  if (bmi < 25) return { label: "Normal", color: "text-primary" };
  if (bmi < 30) return { label: "Overweight", color: "text-accent" };
  return { label: "Obesity", color: "text-destructive" };
}

export default function BMIDisplay({ bmi }: Props) {
  const { label, color } = getBMICategory(bmi);
  const position = Math.min(Math.max(((bmi - 15) / 25) * 100, 0), 100);

  return (
    <div className="rounded-xl bg-card p-6" style={{ boxShadow: "var(--shadow-card)" }}>
      <div className="mb-4 flex items-center gap-2">
        <Activity className="h-5 w-5 text-primary" />
        <h3 className="font-display text-lg font-semibold">BMI Calculator</h3>
      </div>
      <div className="mb-2 text-center">
        <span className="font-display text-4xl font-bold text-foreground">{bmi}</span>
        <span className="ml-1 text-sm text-muted-foreground">kg/m²</span>
      </div>
      <p className={`mb-4 text-center text-lg font-semibold ${color}`}>{label}</p>

      {/* BMI scale bar */}
      <div className="relative mb-1 h-3 w-full overflow-hidden rounded-full bg-muted">
        <div className="absolute inset-0 flex">
          <div className="h-full flex-1 bg-accent/60" />
          <div className="h-full flex-[1.5] bg-primary/60" />
          <div className="h-full flex-1 bg-accent/50" />
          <div className="h-full flex-1 bg-destructive/50" />
        </div>
        <div
          className="absolute top-0 h-full w-1 rounded bg-foreground"
          style={{ left: `${position}%` }}
        />
      </div>
      <div className="flex justify-between text-[10px] text-muted-foreground">
        <span>15</span><span>18.5</span><span>25</span><span>30</span><span>40</span>
      </div>
      <p className="mt-3 text-xs text-muted-foreground text-center">
        Healthy range: 18.5 – 25 kg/m²
      </p>
    </div>
  );
}
