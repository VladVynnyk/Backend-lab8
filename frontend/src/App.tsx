import './App.css'
import Table from "./components/Table/Table.tsx";

function App() {

  return (
      <div className={"mx-auto"}>
          <h1 className="text-3xl font-bold md text-center mb-3">
              Довідник термометрів
          </h1>
          <Table/>
      </div>
  )
}

export default App
