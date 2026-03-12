export interface Recipe {
  Name: string;
  Calories: number;
  FatContent: number;
  SaturatedFatContent: number;
  CholesterolContent: number;
  SodiumContent: number;
  CarbohydrateContent: number;
  FiberContent: number;
  SugarContent: number;
  ProteinContent: number;
  RecipeIngredientParts: string[];
  RecipeInstructions: string[];
  CookTime: string;
  PrepTime: string;
  TotalTime: string;
  image_url?: string;
}

export interface MealGroup {
  meal_name: string;
  recipes: Recipe[];
}

export interface MealPlan {
  bmi: number;
  bmr: number;
  maintain_calories: number;
  target_calories: number;
  meals: MealGroup[];
}

export const NUTRITION_COLUMNS = [
  'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
  'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
] as const;

export type NutritionKey = typeof NUTRITION_COLUMNS[number];

export const WEIGHT_LOSS_PLANS = [
  { label: 'Maintain weight', weight: 1, loss: '-0 kg/week' },
  { label: 'Mild weight loss', weight: 0.9, loss: '-0.25 kg/week' },
  { label: 'Weight loss', weight: 0.8, loss: '-0.5 kg/week' },
  { label: 'Extreme weight loss', weight: 0.6, loss: '-1 kg/week' },
] as const;

export const ACTIVITY_LEVELS = [
  'Little/no exercise',
  'Light exercise',
  'Moderate exercise (3-5 days/wk)',
  'Very active (6-7 days/wk)',
  'Extra active (very active & physical job)',
] as const;
