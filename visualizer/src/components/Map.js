import React, { Component } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN;

class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      lng: mapCenter.longitude,
      lat: props.mapCenter.latitude,
      zoom: props.mapCenter.zoom,
      radius: props.mapCenter.radius
    };
    this.wineryMarkers = [];
  }

  // https://stackoverflow.com/questions/37599561/drawing-a-circle-with-the-radius-in-miles-meters-with-mapbox-gl-js
  createGeoJSONCircle = (center, radiusInKm, points) => {
    if (!points) points = 64;

    var coords = {
      latitude: center[1],
      longitude: center[0]
    };

    var km = radiusInKm;

    var ret = [];
    var distanceX = km / (111.32 * Math.cos(coords.latitude * Math.PI / 180));
    var distanceY = km / 110.574;

    var theta, x, y;
    for (var i = 0; i < points; i++) {
      theta = i / points * (2 * Math.PI);
      x = distanceX * Math.cos(theta);
      y = distanceY * Math.sin(theta);

      ret.push([coords.longitude + x, coords.latitude + y]);
    }
    ret.push(ret[0]);

    return {
      type: "geojson",
      data: {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            geometry: {
              type: "Polygon",
              coordinates: [ret]
            }
          }
        ]
      }
    };
  };

  wineryPopupHTML = wineries => {
    return `<ul>
    <li>
      <strong>Name: </strong> ${wineries.get("wineries").properties.name}
    </li>
    <li>
      <strong>Number of Wines: </strong> ${wineries.get("wineries").properties.numWines}
    </li>
    <li>
      <strong>Average Rating: </strong> ${wineries.get("wineries").properties.avgRate}
    </li>
    <li>
      <strong>Address: </strong> ${wineries.get("wineries").properties.address}
    </li>
    <li>
      <strong>Company Website: </strong> ${wineries.get("wineries").properties.companyWebsite}
    </li>
    <li>
      <strong>Company Email: </strong> ${wineries.get("wineries").properties.email}
    </li>
    <li>
      <strong>Vivino URL: </strong> <a href=${wineries.get("wineries").properties.url} target="_blank"> ${wineries.get("wineries").properties.url} </a> 
    </li>
  </ul>`;
  };

  //-34.59102
  //138.86885
  wineryWinesPopupHTML = (wineries, wines) => {
    wines = wines.map(wine => {
      return wine.get("wines").properties;
    })
    var i;
    var str = `<br><center><h1>Wines:</h1></center><br>`;
    for (i in wines) {
      str = str + `<div style="border-style: solid;">
      <ul>
          <li>
            <strong>Name: </strong> ${wines[i].name}
          </li>
          <li>
            <strong>Grapes: </strong> ${wines[i].grapes}
          </li>
          <li>
            <strong>Style: </strong> ${wines[i].style}
          </li>
          <li>
            <strong>Region: </strong> ${wines[i].region}
          </li>
          <li>
            <strong>Pairings: </strong> ${wines[i].pairing}
          </li>
          <li>
            <strong>Rating: </strong> ${wines[i].rating}
          </li>
          <li>
            <strong>Vivino URL: </strong> <a href=${wines[i].url} target="_blank"> ${wines[i].url} </a> 
          </li>
        </ul>
      </div><br>`;
    }
    return `
    <div style="max-height:300px;max-width:400px;overflow:auto;word-wrap: break-word;">
    <ul>
    <li>
      <strong>Name: </strong> ${wineries.get("wineries").properties.name}
    </li>
    <li>
      <strong>Number of Wines: </strong> ${wineries.get("wineries").properties.numWines}
    </li>
    <li>
      <strong>Average Rating: </strong> ${wineries.get("wineries").properties.avgRate}
    </li>
    <li>
      <strong>Address: </strong> ${wineries.get("wineries").properties.address}
    </li>
    <li>
      <strong>Company Website: </strong> ${wineries.get("wineries").properties.companyWebsite}
    </li>
    <li>
      <strong>Company Email: </strong> ${wineries.get("wineries").properties.email}
    </li>
    <li>
      <strong>Vivino URL: </strong> <a href=${wineries.get("wineries").properties.url} target="_blank"> ${wineries.get("wineries").properties.url} </a> 
    </li>
  </ul>` + str + `</div>`;
  };


  fetchWines (wineries, callback) {
    const session = this.props.driver.session()
    session.run(
        `MATCH (w:Wine {winery: $name})
        RETURN w AS wines;`
      ,
      {name: wineries.get("wineries").properties.name} 
      )
    .then(result => {
      callback(null,result.records);
    }
      )
    .catch(function (error) {
      callback(error,null);
    }); // Return values
    }


  // retrieves results and creates winery markers with popups
  setWineryMarkers() {
    // retrieve winery results from props
    const { wineries } = this.props;
    //remove old winery markers
    this.wineryMarkers.map(m => {
        m.remove();
      return true;
    });

    if (this.props.queryMode === "wineries+wines"){
    this.wineryMarkers = [];
    wineries.map(w => {
    return this.fetchWines(w, (err, results) => {
      if (!err){
        let out = this.createMarker(w, results);
        this.wineryMarkers.push(out);
      } else {
        console.log(err);
      }
      return true;
    })
  });
}
    else {
    //add the new winery markers
    this.wineryMarkers = wineries.map(w => {
      return this.createMarker(w, null);
    });
  }
}

  // create mapbox marker
  createMarker(w, wines) {
    return new mapboxgl.Marker()
    .setLngLat([w.get("wineries").properties.longitude , w.get("wineries").properties.latitude])
    .setPopup(
      new mapboxgl.Popup({ offset: 25 }).setHTML(
        this.props.queryMode === "wineries+wines"? this.wineryWinesPopupHTML(w, wines):this.wineryPopupHTML(w))
    )
    .addTo(this.map);
  }

  // checks to see if the query circle changed radius or location
  componentDidUpdate() {
    this.setWineryMarkers();
    if (this.mapLoaded) {
      this.map
        .getSource("polygon")
        .setData(
          this.createGeoJSONCircle(
            [this.props.mapCenter.longitude, this.props.mapCenter.latitude],
            this.props.mapCenter.radius
          ).data
        );
    }
  }

  componentDidMount() {
    const { lng, lat, zoom } = this.state;

    this.map = new mapboxgl.Map({
      container: this.mapContainer,
      style: "mapbox://styles/mapbox/streets-v9",
      center: [lng, lat],
      zoom
    });

    this.map.on("load", () => {
      this.mapLoaded = true;
      this.map.addSource(
        "polygon",
        this.createGeoJSONCircle([lng, lat], this.props.mapCenter.radius)
      );
      this.map.addLayer({
        id: "polygon",
        type: "fill",
        source: "polygon",
        layout: {},
        paint: {
          "fill-color": "blue",
          "fill-opacity": 0.6
        }
      });
    });

    const onDragEnd = e => {
      var lngLat = e.target.getLngLat();

      const viewport = {
        latitude: lngLat.lat,
        longitude: lngLat.lng,
        zoom: this.map.getZoom()
      };
      this.props.mapSearchPointChange(viewport);

      this.map
        .getSource("polygon")
        .setData(
          this.createGeoJSONCircle(
            [lngLat.lng, lngLat.lat],
            this.props.mapCenter.radius
          ).data
        );
    };

    new mapboxgl.Marker({ color: "red", zIndexOffset: 9999 })
      .setLngLat([lng, lat])
      .addTo(this.map)
      .setPopup(
        new mapboxgl.Popup().setText(
          "Drag me to search for wineries in this area! Also, try changing the query radius."
        )
      )
      .setDraggable(true)
      .on("dragend", onDragEnd)
      .addTo(this.map)
      .togglePopup();

    this.map.on("move", () => {
      const { lng, lat } = this.map.getCenter();

      this.setState({
        lng: lng,
        lat: lat,
        zoom: this.map.getZoom().toFixed(2),
        radius: this.props.mapCenter.radius
      });
    });
    this.setWineryMarkers();
  }


  render() {
    return (
      <div>
        <div
          ref={el => (this.mapContainer = el)}
          className="absolute top right left bottom"
        />
      </div>
    );
  }
}

export default Map;
