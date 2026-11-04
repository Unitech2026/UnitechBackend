import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadStudents() {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/students`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          throw new Error(`Error HTTP ${response.status}`);
        }

        const data = await response.json();
        if (!Array.isArray(data)) {
          throw new Error("La respuesta no contiene una lista de alumnos.");
        }
        setStudents(data);
      } catch (err) {
        if (err.name !== "AbortError") {
          setError("No se pudieron cargar los alumnos.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    loadStudents();

    return () => controller.abort();
  }, []);

  return (
    <main>
      <h1>Listado de alumnos</h1>

      {loading && <p role="status">Cargando alumnos...</p>}

      {error && <p role="alert">{error}</p>}

      {!loading && !error && (
        <>
          <p>Total de alumnos: {students.length}</p>

          {students.length === 0 ? (
            <p>No hay alumnos registrados.</p>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Matrícula</th>
                    <th scope="col">Nombre</th>
                  </tr>
                </thead>

                <tbody>
                  {students.map((student) => (
                    <tr key={student.id}>
                      <td>{student.id}</td>
                      <td>{student.matricula}</td>
                      <td>{student.nombre}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </main>
  );
}

export default App;
