import { useState, useMemo } from "react";
import { ACTIVITY_LEVELS, WEIGHT_LOSS_PLANS, NUTRITION_COLUMNS } from "@/types/recipe";
import type { MealPlan, Recipe, NutritionKey } from "@/types/recipe";
import { generateMealPlan, ApiError } from "@/lib/api";
import BMIDisplay from "@/components/BMIDisplay";
import CaloriesDisplay from "@/components/CaloriesDisplay";
import RecipeCard from "@/components/RecipeCard";
import NutritionPieChart from "@/components/NutritionPieChart";
import { Loader2 } from "lucide-react";

export default function DietRecommendation() {
  const [form, setForm] = useState({
    age: 25, height: 175, weight: 70, gender: "Male" as "Male" | "Female",
    activity: ACTIVITY_LEVELS[2], plan: WEIGHT_LOSS_PLANS[0].label, meals: 3 as 3 | 4 | 5,
  });
  const [mealPlan, setMealPlan] = useState<MealPlan | null>(null);
  const [selectedPerMeal, setSelectedPerMeal] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await generateMealPlan({
        age: form.age,
        height: form.height,
        weight: form.weight,
        gender: form.gender,
        activity: form.activity,
        number_of_meals: form.meals,
        weight_loss: form.plan,
      });
      setMealPlan(data);
      const initial: Record<string, string> = {};
      data.meals.forEach((meal) => {
        if (meal.recipes[0]) initial[meal.meal_name] = meal.recipes[0].Name;
      });
      setSelectedPerMeal(initial);
    } catch (err) {
      const message = err instanceof ApiError
        ? `Server error ${err.status}: ${err.message}`
        : "Unexpected error. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const update = (key: string, value: string | number) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const summedNutrition = useMemo((): Record<NutritionKey, number> | null => {
    if (!mealPlan) return null;
    const sum = Object.fromEntries(NUTRITION_COLUMNS.map((c) => [c, 0])) as Record<NutritionKey, number>;
    mealPlan.meals.forEach((meal) => {
      const recipe = meal.recipes.find((r) => r.Name === selectedPerMeal[meal.meal_name]);
      if (recipe) {
        NUTRITION_COLUMNS.forEach((col) => {
          sum[col] += recipe[col as keyof Recipe] as number;
        });
      }
    });
    return sum;
  }, [mealPlan, selectedPerMeal]);

  const hasSelections = Object.keys(selectedPerMeal).length > 0;

  return (
    <div className="container py-8">
      <h1 className="mb-2 font-display text-3xl font-bold text-foreground">
        💪 Automatic Diet Recommendation
      </h1>
      <p className="mb-8 text-muted-foreground">
        Enter your details to generate a personalized meal plan.
      </p>

      <form onSubmit={handleGenerate} className="mb-10 rounded-xl bg-card p-6" style={{ boxShadow: "var(--shadow-card)" }}>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {/* Age */}
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">Age</span>
            <input type="number" min={2} max={120} value={form.age}
              onChange={(e) => update("age", +e.target.value)}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring"
            />
          </label>
          {/* Height */}
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">Height (cm)</span>
            <input type="number" min={50} max={300} value={form.height}
              onChange={(e) => update("height", +e.target.value)}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring"
            />
          </label>
          {/* Weight */}
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">Weight (kg)</span>
            <input type="number" min={10} max={300} value={form.weight}
              onChange={(e) => update("weight", +e.target.value)}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring"
            />
          </label>
          {/* Gender */}
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">Gender</span>
            <select value={form.gender} onChange={(e) => update("gender", e.target.value)}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring">
              <option>Male</option>
              <option>Female</option>
            </select>
          </label>
          {/* Activity */}
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">Activity Level</span>
            <select value={form.activity} onChange={(e) => update("activity", e.target.value)}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring">
              {ACTIVITY_LEVELS.map((a) => <option key={a}>{a}</option>)}
            </select>
          </label>
          {/* Plan */}
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">Weight Loss Plan</span>
            <select value={form.plan} onChange={(e) => update("plan", e.target.value)}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring">
              {WEIGHT_LOSS_PLANS.map((p) => <option key={p.label}>{p.label}</option>)}
            </select>
          </label>
          {/* Meals per day */}
          <label className="space-y-1.5 sm:col-span-2 lg:col-span-3">
            <span className="text-sm font-medium text-foreground">Meals per day: {form.meals}</span>
            <input type="range" min={3} max={5} value={form.meals}
              onChange={(e) => update("meals", +e.target.value as 3 | 4 | 5)}
              className="w-full accent-primary"
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>3</span><span>4</span><span>5</span>
            </div>
          </label>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="mt-6 inline-flex items-center gap-2 rounded-lg bg-primary px-8 py-3 font-medium text-primary-foreground transition-transform hover:scale-105 disabled:opacity-60"
        >
          {loading && <Loader2 className="h-4 w-4 animate-spin" />}
          Generate Meal Plan
        </button>
      </form>

      {error && (
        <div className="mb-6 rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
          {error}
        </div>
      )}

      {mealPlan && (
        <div className="animate-fade-in space-y-8">
          {/* BMI + Calories */}
          <div className="grid gap-6 md:grid-cols-2">
            <BMIDisplay bmi={mealPlan.bmi} />
            <CaloriesDisplay maintainCalories={mealPlan.maintain_calories} />
          </div>

          {/* Meal recommendations */}
          <div>
            <h2 className="mb-2 font-display text-2xl font-bold text-foreground">
              🍽️ Your Meal Plan
            </h2>
            <p className="mb-6 text-sm text-muted-foreground">
              Click a recipe to select it for your daily nutrition summary.
            </p>
            <div className="space-y-8">
              {mealPlan.meals.map((meal) => (
                <div key={meal.meal_name}>
                  <h3 className="mb-3 font-display text-xl font-semibold capitalize text-primary">
                    {meal.meal_name}
                  </h3>
                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {meal.recipes.map((recipe) => {
                      const isSelected = selectedPerMeal[meal.meal_name] === recipe.Name;
                      return (
                        <div
                          key={recipe.Name}
                          onClick={() => setSelectedPerMeal((prev) => ({ ...prev, [meal.meal_name]: recipe.Name }))}
                          className={`cursor-pointer rounded-xl ring-2 transition-all ${isSelected ? "ring-primary" : "ring-transparent hover:ring-primary/30"}`}
                        >
                          <RecipeCard recipe={recipe} />
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Nutritional Overview for selected meals */}
          {hasSelections && summedNutrition && (
            <div className="rounded-xl bg-card p-6" style={{ boxShadow: "var(--shadow-card)" }}>
              <h2 className="mb-1 font-display text-2xl font-bold text-foreground">
                📊 Nutritional Overview
              </h2>
              <p className="mb-2 text-sm text-muted-foreground">
                Sum of your selected recipes across all meals.
              </p>
              <p className="mb-4 text-lg font-semibold text-primary">
                Total: {Math.round(summedNutrition.Calories)} kcal
              </p>
              <NutritionPieChart nutritionData={summedNutrition} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
