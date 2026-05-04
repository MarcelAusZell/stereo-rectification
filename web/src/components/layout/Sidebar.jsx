const links = [
  { id: "introduction", title: "Introduction" },
  { id: "epipolar-geometry", title: "Epipolar Geometry" },
];

export default function Sidebar() {
  return (
    <div className="card bg-base-200">
      <div className="card-body p-4">
        <h2 className="card-title text-base">Contents</h2>

        <ul className="menu">
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