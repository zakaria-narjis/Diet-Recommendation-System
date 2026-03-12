import { Flame } from "lucide-react";
import { WEIGHT_LOSS_PLANS } from "@/types/recipe";

interface Props {
  maintainCalories: number;
}

export default function CaloriesDisplay({ maintainCalories }: Props) {
  return (
    <div className="rounded-xl bg-card p-6" style={{ boxShadow: "var(--shadow-card)" }}>
      <div className="mb-4 flex items-center gap-2">
        <Flame className="h-5 w-5 text-accent" />
        <h3 className="font-display text-lg font-semibold">Calorie Targets</h3>
      </div>
      <p className="mb-4 text-sm text-muted-foreground">
        Daily calorie estimates for your weight management goals.
      </p>
      <div className="grid grid-cols-2 gap-3">
        {WEIGHT_LOSS_PLANS.map((plan) => {
          const cals = Math.round(maintainCalories * plan.weight);
          return (
            <div key={plan.label} className="rounded-lg bg-muted p-3 text-center">
              <div className="text-xs font-medium text-muted-foreground">{plan.label}</div>
              <div className="mt-1 font-display text-xl font-bold text-foreground">{cals}</div>
              <div className="text-[11px] text-primary">{plan.loss}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
