import { NavBar } from "@/components/layout/NavBar";
import { TechnologyClient } from "./TechnologyClient";
import { getTechnologyData } from "@/lib/api";

export default async function TechnologyPage() {
  const data = await getTechnologyData();

  return (
    <>
      <NavBar
        title="Technology Comparison"
        subtitle="Side-by-side analysis of renewable energy technologies for construction"
      />
      <div className="flex-1 p-6 overflow-auto">
        <TechnologyClient data={data} />
      </div>
    </>
  );
}
