import Sidebar from "./components/layout/Sidebar";
import Intro from "./components/sections/Intro";
import EpipolarGeometry from "./components/sections/EpipolarGeometry";


export default function App() {
  return (
    <div className="drawer lg:drawer-open">
      <input id="toc-drawer" type="checkbox" className="drawer-toggle" />

      <div className="drawer-content">
        <div className="grid grid-cols-1 gap-8 p-6 lg:grid-cols-[16rem_1fr]">
          
          {/* Desktop sidebar */}
          <aside className="hidden lg:block lg:sticky lg:top-6 lg:self-start">
            <Sidebar />
          </aside>

          <main className="space-y-24">
            {/* Mobile toggle */}
            <label
              htmlFor="toc-drawer"
              className="btn btn-primary drawer-button lg:hidden sticky top-4 z-10"
            >
              Inhalt
            </label>

            {/* Sections */}
            <Intro />
            <EpipolarGeometry/>

          </main>
        </div>
      </div>

      {/* Mobile drawer */}
      <div className="drawer-side lg:hidden">
        <label htmlFor="toc-drawer" className="drawer-overlay"></label>

        <aside className="min-h-full w-72 bg-base-100 p-4">
          <Sidebar />
        </aside>
      </div>
    </div>
  );
}