const links = [
  { id: "introduction", title: "Introduction" },
  { id: "epipolar-constraint", title: "Epipolar Constraint" },
  { id: "epipolar-lines", title: "Epipolar Lines" },
];

import "./MobileDrawer.css"


export default function MobileDrawer() {
  return (
    <label
      htmlFor="toc-drawer"
      className="btn sticky top-4 z-10 mb-8 lg:hidden opacity-50 text-red-300"
    >
      <svg
        className="swap-off fill-current"
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="32"
        viewBox="0 0 512 512">
        <path d="M64,384H448V341.33H64Zm0-106.67H448V234.67H64ZM64,128v42.67H448V128Z" />
      </svg>
    </label>
  );
}

MobileDrawer.Side = function MobileDrawerSide() {
  return (
    <div className="drawer-side lg:hidden">
      <label htmlFor="toc-drawer" className="drawer-overlay"></label>
      <aside className="min-h-full w-72 bg-base-100 p-4">
        <ul className="menu p-0 text-[15px]">
          {links.map((link) => (
            <li key={link.id}>
              <a href={`#${link.id}`}>{link.title}</a>
            </li>
          ))}
        </ul>
      </aside>
    </div>
  );
};