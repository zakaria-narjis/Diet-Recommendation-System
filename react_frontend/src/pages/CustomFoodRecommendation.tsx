import { useState } from "react";
import { predictRecipes, ApiError } from "@/lib/api";
import type { Recipe } from "@/types/recipe";
import { NUTRITION_COLUMNS, type NutritionKey } from "@/types/recipe";
import RecipeCard from "@/components/RecipeCard";
import NutritionPieChart from "@/components/NutritionPieChart";
import { Loader2 } from "lucide-react";

const SLIDERS = [
  { key: "Calories", min: 0, max: 2000, default: 500, unit: "cal" },
  { key: "FatContent", min: 0, max: 100, default: 50, unit: "g" },
  { key: "SaturatedFatContent", min: 0, max: 13, default: 0, unit: "g" },
  { key: "CholesterolContent", min: 0, max: 300, default: 0, unit: "mg" },
  { key: "SodiumContent", min: 0, max: 2300, default: 400, unit: "mg" },
  { key: "CarbohydrateContent", min: 0, max: 325, default: 100, unit: "g" },
  { key: "FiberContent", min: 0, max: 50, default: 10, unit: "g" },
  { key: "SugarContent", min: 0, max: 40, default: 10, unit: "g" },
  { key: "ProteinContent", min: 0, max: 40, default: 10, unit: "g" },
] as const;

export default function CustomFoodRecommendation() {
  const [values, setValues] = useState<Record<string, number>>(
    Object.fromEntries(SLIDERS.map((s) => [s.key, s.default]))
  );
  const [nbRecs, setNbRecs] = useState(5);
  const [ingredients, setIngredients] = useState("");
  const [results, setResults] = useState<Recipe[] | null>(null);
  const [selectedRecipe, setSelectedRecipe] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const nutrition_input = [
        values.Calories, values.FatContent, values.SaturatedFatContent,
        values.CholesterolContent, values.SodiumContent, values.CarbohydrateContent,
        values.FiberContent, values.SugarContent, values.ProteinContent,
      ] as [number, number, number, number, number, number, number, number, number];

      const recs = await predictRecipes({
        nutrition_input,
        ingredients: ingredients.split(";").map((s) => s.trim()).filter(Boolean),
        params: { n_neighbors: nbRecs, return_distance: false },
      });
      setResults(recs);
      setSelectedRecipe(recs[0]?.Name ?? "");
    } catch (err) {
      const message = err instanceof ApiError
        ? `Server error ${err.status}: ${err.message}`
        : "Unexpected error. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const activeRecipe = results?.find((r) => r.Name === selectedRecipe);
  const activeNutritionData = activeRecipe
    ? Object.fromEntries(NUTRITION_COLUMNS.map((col) => [col, activeRecipe[col as keyof Recipe] as number])) as Record<NutritionKey, number>
    : null;

  return (
    <div className="container py-8">
      <h1 className="mb-2 font-display text-3xl font-bold text-foreground">
        🔍 Custom Food Recommendation
      </h1>
      <p className="mb-8 text-muted-foreground">
        Set your target nutritional values and optionally filter by ingredients.
      </p>

      <form onSubmit={handleGenerate} className="mb-10 rounded-xl bg-card p-6" style={{ boxShadow: "var(--shadow-card)" }}>
        <h2 className="mb-4 font-display text-lg font-semibold text-foreground">Nutritional Values</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {SLIDERS.map((s) => (
            <label key={s.key} className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="font-medium text-foreground">{s.key.replace('Content', '')}</span>
                <span className="text-muted-foreground">{values[s.key]}{s.unit || ''}</span>
              </div>
              <input
                type="range" min={s.min} max={s.max} value={values[s.key]}
                onChange={(e) => setValues((v) => ({ ...v, [s.key]: +e.target.value }))}
                className="w-full accent-primary"
              />
            </label>
          ))}
        </div>

        <div className="mt-6 space-y-4">
          <h2 className="font-display text-lg font-semibold text-foreground">Options</h2>
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">
              Number of recommendations: {nbRecs}
            </span>
            <input type="range" min={5} max={20} step={5} value={nbRecs}
              onChange={(e) => setNbRecs(+e.target.value)}
              className="w-full accent-primary"
            />
          </label>
          <label className="space-y-1.5">
            <span className="text-sm font-medium text-foreground">
              Ingredients (separate with ";")
            </span>
            <input
              type="text"
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
              placeholder="Milk;eggs;butter;chicken..."
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring"
            />
            <span className="text-xs text-muted-foreground">Example: Milk;eggs;butter;chicken</span>
          </label>
        </div>

        <button
          type="submit" disabled={loading}
          className="mt-6 inline-flex items-center gap-2 rounded-lg bg-primary px-8 py-3 font-medium text-primary-foreground transition-transform hover:scale-105 disabled:opacity-60"
        >
          {loading && <Loader2 className="h-4 w-4 animate-spin" />}
          Generate
        </button>
      </form>

      {error && (
        <div className="mb-6 rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
          {error}
        </div>
      )}

      {results && results.length === 0 && (
        <div className="rounded-xl bg-card p-12 text-center text-muted-foreground" style={{ boxShadow: "var(--shadow-card)" }}>
          No recipes found. Try adjusting your nutritional targets or ingredients.
        </div>
      )}

      {results && results.length > 0 && (
        <div className="animate-fade-in space-y-8">
          <div>
            <h2 className="mb-4 font-display text-2xl font-bold text-foreground">
              Recommended Recipes
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {results.map((r) => (
                <RecipeCard key={r.Name} recipe={r} />
              ))}
            </div>
          </div>

          {/* Overview chart */}
          <div className="rounded-xl bg-card p-6" style={{ boxShadow: "var(--shadow-card)" }}>
            <h2 className="mb-4 font-display text-xl font-semibold text-foreground">
              Nutritional Overview
            </h2>
            <div className="mb-4 flex justify-center">
              <select
                value={selectedRecipe}
                onChange={(e) => setSelectedRecipe(e.target.value)}
                className="rounded-lg border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring"
              >
                {results.map((r) => (
                  <option key={r.Name} value={r.Name}>{r.Name}</option>
                ))}
              </select>
            </div>
            {activeNutritionData && <NutritionPieChart nutritionData={activeNutritionData} />}
          </div>
        </div>
      )}
    </div>
  );
}
