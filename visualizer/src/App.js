import React, { Component } from "react";
import "./App.css";
import Map from "./components/Map";
import neo4j from "neo4j-driver/lib/browser/neo4j-web";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      wineries: [],
      loaded: false,
      queryMode: "wineries",
      selectedWinery: false,
      mapCenter: {
        latitude: 41.8336652355739,
        longitude: -119.967368054181,
        radius: 100,
        zoom: 4
      }
    };

    this.driver = neo4j.driver(
      process.env.REACT_APP_NEO4J_URI,
      neo4j.auth.basic(
        process.env.REACT_APP_NEO4J_USER,
        process.env.REACT_APP_NEO4J_PASSWORD
      )
      ,
      { encrypted: false }
    );

    
    this.fetchWineries();
  }

  winerySelected = w => {
    this.setState({
      selectedWinery: w
    });
  };

  mapSearchPointChange = viewport => {
    this.setState({
      mapCenter: {
        ...this.state.mapCenter,
        latitude: viewport.latitude,
        longitude: viewport.longitude,
        zoom: viewport.zoom
      }
    });
  };
   
  fetchWineries = () => {
    const session = this.driver.session();
    const { mapCenter } = this.state;
    session
      .run(
        `MATCH (w:Winery)
        WHERE w.latitude <> 'N/A' OR w.longitude <> 'N/A'
        WITH distance(point({latitude: toFloat(w.latitude), longitude: toFloat(w.longitude)}), point({latitude: $lat, longitude: $long})) AS d, w
        WHERE d < ($radius * 1000)
        RETURN w AS wineries;`
      ,
      {
        lat: mapCenter.latitude,
        long: mapCenter.longitude,
        radius: mapCenter.radius
      }
      )
      .then(result => {
        console.log(result.records);
        const wineries = result.records;
        this.setState({
          wineries,
          loaded: true
        });
        session.close();
      })
      .catch(e => {
        console.log(e);
        session.close();
      });
  };

  radiusChange = e => {
    this.setState(
      {
        mapCenter: {
          ...this.state.mapCenter,
          radius: Number(e.target.value)
        }
      },
      () => {
        this.fetchWineries();
      }
    );
  };

  componentDidUpdate = (prevProps, prevState) => {
    if (
      this.state.mapCenter.latitude !== prevState.mapCenter.latitude ||
      this.state.mapCenter.longitude !== prevState.mapCenter.longitude
    ) {
      this.fetchWineries();
    }
    if (
      this.state.selectedWinery &&
      (!prevState.selectedWinery ||
        this.state.selectedWinery.name !== prevState.selectedWinery.name ||
        false ||
        false)
    ) {
    }
  };

  handleSubmit = () => {};

  handleQueryChange = event => {
    const target = event.target;
    const value = target.value;
    this.setState(
      {
        queryMode: value
      },
      () => console.log(this.state.queryMode)
    );
  };

  content() {
    return (
    <div id="app-wrapper">
        <div id="app-toolbar">
          <form action="" onSubmit={this.handleSubmit}>
            <div className="row tools">
              <div className="col-sm-2">
                <div className="tool radius">
                  <h5>Query Radius</h5>
                  <input
                    type="number"
                    id="radius-value"
                    className="form-control"
                    min="0.1"
                    max="2.0"
                    step="0.1"
                    value={this.state.mapCenter.radius}
                    onChange={this.radiusChange}
                  />
                  <select className="form-control" id="radius-suffix">
                    <option value="km">km</option>
                  </select>
                </div>
              </div>

              <div className="col-sm-2">
                <div className="tool coordinates">
                  <h5>Latitude</h5>
                  <input
                    type="number"
                    step="any"
                    id="coordinates-lat"
                    className="form-control"
                    placeholder="Latitude"
                    value={this.state.mapCenter.latitude}
                    onChange={()=>(true)}
                  />
                </div>
              </div>

              <div className="col-sm-2">
                <div className="tool coordinates">
                  <h5>Longitude</h5>
                  <input
                    type="number"
                    step="any"
                    id="coordinates-lng"
                    className="form-control"
                    placeholder="Longitude"
                    value={this.state.mapCenter.longitude}
                    onChange={()=>true}
                  />
                </div>
              </div>

              <h2>Query By:</h2>
          <div className="row">
            <fieldset>
                <input
                  type="radio"
                  id="wineries"
                  name="wineries"
                  value="wineries"
                  checked={this.state.queryMode === "wineries"}
                  onChange={this.handleQueryChange}
                />
                <label>Wineries</label>
                <input
                  type="radio"
                  id="wineries+wines"
                  name="wineries+wines"
                  value="wineries+wines"
                  checked={this.state.queryMode === "wineries+wines"}
                  onChange={this.handleQueryChange}
                />
                <label>Wineries + wines</label>
            </fieldset>
          </div>

            </div>
          </form>
        </div>
        <div className="chart-wrapper">
          <div id="app-maparea">
            <Map
              mapSearchPointChange={this.mapSearchPointChange}
              mapCenter={this.state.mapCenter}
              wineries={this.state.wineries}
              winerySelected={this.winerySelected}
              selectedWinery={this.state.selectedWinery}
              driver={this.driver}
              queryMode={this.state.queryMode}
            />
          </div>
        </div>

      </div>
    )
  }

  render() {
    return (
      <div>
    {this.state.loaded ? this.content() : null}
    </div>
    );
  }
}

export default App;
