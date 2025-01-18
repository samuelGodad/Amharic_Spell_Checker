import {CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import "./App.css";
import Header from "./components/Layout/Header";
import Footer from "./components/Layout/Footer";
import AmharicEditor from "./components/Editor/AmharicEditor";
const theme = createTheme({
  palette: {
    // mode: "dark",
    primary: {
      main: "#d82929",
    },
  },
});

function App() {

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header />
      <div className="App">
        <h1 className="title">Amharic Editor</h1>
        <AmharicEditor />
      </div>
      <Footer />
    </ThemeProvider>
  );
}

export default App;
