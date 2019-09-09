export interface TileData {
    projectNumber: number
    projectName: string
    previousTrainedModel: string
    rows: number
    cols: number
    comments: string
    model: ModelData[]
}

export interface ModelData {
    name: string
    status: string
}