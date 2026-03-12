import { Link } from "react-router-dom";
import { Dumbbell, Search, Leaf, ArrowRight } from "lucide-react";
import heroImage from "@/assets/hero-food.jpg";

const Index = () => {
  return (
    <div className="min-h-[calc(100vh-4rem)]">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-secondary/50" />
        <div className="container relative grid items-center gap-8 py-16 md:grid-cols-2 md:py-24">
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
              <Leaf className="h-4 w-4" />
              AI-Powered Nutrition
            </div>
            <h1 className="font-display text-4xl font-bold leading-tight text-foreground md:text-5xl lg:text-6xl">
              Your Personal<br />
              <span className="text-primary">Diet Planner</span>
            </h1>
            <p className="max-w-md text-lg text-muted-foreground">
              Generate personalized meal plans based on your health metrics, or search 500K+ recipes by nutritional targets.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                to="/diet"
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-6 py-3 font-medium text-primary-foreground transition-transform hover:scale-105"
              >
                <Dumbbell className="h-4 w-4" /> Get Diet Plan <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                to="/custom"
                className="inline-flex items-center gap-2 rounded-lg border bg-card px-6 py-3 font-medium text-foreground transition-colors hover:bg-muted"
              >
                <Search className="h-4 w-4" /> Custom Search
              </Link>
            </div>
          </div>
          <div className="flex justify-center">
            <img
              src={heroImage}
              alt="Fresh healthy ingredients"
              className="w-full max-w-lg rounded-2xl object-cover"
              style={{ boxShadow: "var(--shadow-card-hover)" }}
            />
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="border-t bg-card py-16">
        <div className="container">
          <h2 className="mb-10 text-center font-display text-3xl font-bold text-foreground">
            How It Works
          </h2>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              { icon: "📊", title: "Enter Your Metrics", desc: "Provide age, weight, height, and activity level to calculate your nutritional needs." },
              { icon: "🤖", title: "AI Finds Recipes", desc: "Our engine uses cosine similarity over nutritional vectors across 500K+ recipes." },
              { icon: "🍽️", title: "Get Your Plan", desc: "Receive a personalized meal plan with detailed nutritional breakdowns and instructions." },
            ].map((f) => (
              <div key={f.title} className="rounded-xl border bg-background p-6 text-center transition-all hover:border-primary/30" style={{ boxShadow: "var(--shadow-card)" }}>
                <div className="mb-3 text-4xl">{f.icon}</div>
                <h3 className="mb-2 font-display text-lg font-semibold text-foreground">{f.title}</h3>
                <p className="text-sm text-muted-foreground">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Index;
