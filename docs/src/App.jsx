import Sidebar from "./components/layout/Sidebar";
import Intro from "./components/sections/Intro";
import EpipolarGeometry from "./components/sections/EpipolarGeometry";
import "./App.css"

export default function App() {
  return (
    <div className="drawer lg:drawer-open">
      <input id="toc-drawer" type="checkbox" className="drawer-toggle" />

      <div className="drawer-content">
        {/* one main container */}
        <div className="flex min-h-screen">
          {/* desktop sidebar container */}
          <aside className="sidebar-container hidden w-auto shrink-0 p-6 lg:block">
            <div className="sticky top-6">
              <Sidebar />
            </div>
          </aside>

          {/* content container */}
          <main className="flex-1 px-2 py-4 lg:px-8 lg:py-8">
            {/* mobile drawer toggle */}
            <label
              htmlFor="toc-drawer"
              className="btn btn-primary drawer-button sticky top-4 z-10 mb-8 lg:hidden"
            >
              Content
            </label>

            {/* centered section container */}
            <div className="section-container w-[80%] space-y-24 lg:w-[60%]">
              <Intro />
              <EpipolarGeometry />
            </div>
          </main>
        </div>
      </div>

      {/* mobile drawer */}
      <div className="drawer-side lg:hidden">
        <label htmlFor="toc-drawer" className="drawer-overlay"></label>

        <aside className="min-h-full w-72 bg-base-100 p-4">
          <Sidebar />
        </aside>
      </div>
    </div>
  );
}