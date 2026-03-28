import { NavBar } from "@/components/layout/NavBar";
import { BenchmarkingClient } from "./BenchmarkingClient";
import { getBenchmarkData } from "@/lib/api";

export default async function BenchmarkingPage() {
  const data = await getBenchmarkData();

  return (
    <>
      <NavBar
        title="Competitive Benchmarking"
        subtitle="Peer case studies and competitive landscape analysis"
      />
      <div className="flex-1 p-6 overflow-auto">
        <BenchmarkingClient data={data} />
      </div>
    </>
  );
}
