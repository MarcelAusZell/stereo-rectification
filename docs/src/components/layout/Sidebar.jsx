const links = [
  { id: "introduction", title: "Introduction" },
  { id: "epipolar-geometry", title: "Epipolar Geometry" },
];

export default function Sidebar() {
  return (
    <div className="card bg-base-200">
      <div className="card-body p-4">
        <h2 className="card-title font-bold text-xl text-red-400">Contents</h2>

        <ul className="menu p-0 text-[15px]">
          {links.map((link) => (
            <li key={link.id}>
              <a href={`#${link.id}`}>{link.title}</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}