import Sidebar from "./components/layout/Sidebar";
import MobileDrawer from "./components/layout/MobileDrawer";
import Intro from "./components/sections/Intro";
import EpipolarConstraint from "./components/sections/EpipolarConstraint";
import EpipolarLines from "./components/sections/EpipolarLines";
import "./App.css";

export default function App() {
  return (
    <div className="drawer lg:drawer-open">
      <input id="toc-drawer" type="checkbox" className="drawer-toggle" />

      <div className="drawer-content">
        <div className="flex min-h-screen">
          <aside className="sidebar-container hidden shrink-0 p-6 lg:block">
            <div className="sticky top-6">
              <Sidebar />
            </div>
          </aside>

          <main className="flex-1 px-2 py-4 lg:px-8 lg:py-8">
            <MobileDrawer />

            <div className="section-container w-[80%] space-y-24 lg:w-[60%]">
              <Intro />
              <EpipolarConstraint />
              <EpipolarLines />
            </div>
          </main>
        </div>
      </div>

      <MobileDrawer.Side />
    </div>
  );
}