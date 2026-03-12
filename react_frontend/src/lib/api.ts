import type { Recipe, MealPlan } from "@/types/recipe";

const BASE_URL = import.meta.env.VITE_API_URL ?? "";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new ApiError(res.status, body);
  }
  return res.json() as Promise<T>;
}

export interface PredictRequest {
  nutrition_input: [number, number, number, number, number, number, number, number, number];
  ingredients: string[];
  params: { n_neighbors: number; return_distance: false };
}

export interface MealPlanRequest {
  age: number;
  height: number;
  weight: number;
  gender: "Male" | "Female";
  activity: string;
  number_of_meals: 3 | 4 | 5;
  weight_loss: string;
}

export async function predictRecipes(req: PredictRequest): Promise<Recipe[]> {
  const data = await apiFetch<{ output: Recipe[] | null }>("/predict/", {
    method: "POST",
    body: JSON.stringify(req),
  });
  return data.output ?? [];
}

export async function generateMealPlan(req: MealPlanRequest): Promise<MealPlan> {
  return apiFetch<MealPlan>("/generate-meal-plan/", {
    method: "POST",
    body: JSON.stringify(req),
  });
}
