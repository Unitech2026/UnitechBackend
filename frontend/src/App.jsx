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

      {loading && <p>Cargando alumnos...</p>}

      {error && <p role="alert">{error}</p>}

      {!loading && !error && (
        <>
          <p>Total de alumnos: {students.length}</p>

          {students.length === 0 ? (
            <p>No hay alumnos registrados.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Matrícula</th>
                  <th>Nombre</th>
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
          )}
        </>
      )}
    </main>
  );
}

export default App;