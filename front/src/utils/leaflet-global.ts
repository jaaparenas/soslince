import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Asignar L a window/globalThis para que vue-leaflet-markercluster lo encuentre
;(window as any).L = L

export default L
