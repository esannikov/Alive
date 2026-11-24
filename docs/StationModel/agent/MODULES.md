# Карта модулів станції

Цю карту оновлює `npm run build`. Перелік відповідає авторському дереву StationModel/source. Для послідовності складання відкрий [довідник](../STATION_AGENT_GUIDE.md).

## Фізична ієрархія

| Ярус | ID для камери й маркерів | Групи моделі |
|---|---|---|
| Оболонка і купол | `roof` | `dome.domeRoofGroup`, `rings.roofVaultGroup` |
| III · Верхнє кільце | `third` | `rings.thirdLevelGroup` |
| II · Парк і площа | `upper` | `dome.habitatGroup`, `rings.habitatGroup` |
| I · B1 · Комунікації | `utility` | `utility.group` |
| I · B2 · Вантажі | `cargo` | `cargo.group` |
| I · B3 · Бази й ангари | `refugee` | `lower.b3Group` |
| I · B4 · Інженерна палуба й кіль | `subbase` | `lower.b4Group` |

## Вхідні модулі

Ліворуч — файл. Праворуч — усі файли проєкту, які безпосередньо його імпортують. Початок збірки — `src/main.js`.

| Файл | Хто підключає |
|---|---|
| `src/architecture/berthKit.js` | `src/architecture/dockFront.js`, `src/architecture/freightCruiser.js`, `src/architecture/portTender.js`, `src/architecture/readingHall.js`, `src/architecture/shieldShell.js`, `src/layers/third/docks.js` |
| `src/architecture/bridgeUses.js` | `src/main.js`, `src/navigation/cameras.js` |
| `src/architecture/dockFront.js` | `src/layers/residentialRings.js`, `src/layers/third/docks.js` |
| `src/architecture/dockGraphics.js` | `src/architecture/dockFront.js`, `src/architecture/freightCruiser.js`, `src/architecture/portTender.js` |
| `src/architecture/finishes.js` | `src/architecture/plazaGallery.js`, `src/layers/domeAndFountain.js` |
| `src/architecture/flightSkin.js` | `src/architecture/hullInlays.js`, `src/layers/cargoLayer.js`, `src/layers/lower/b4/keel.js`, `src/layers/refugeeLayer.js`, `src/layers/residentialRings.js` |
| `src/architecture/freightCruiser.js` | `src/layers/third/docks.js` |
| `src/architecture/hullInlays.js` | `src/layers/residentialRings.js` |
| `src/architecture/keelGirders.js` | `src/layers/residentialRings.js` |
| `src/architecture/lawScreen.js` | `src/layers/domeAndFountain.js`, `src/navigation/cameras.js` |
| `src/architecture/libraryWindow.js` | `src/layers/residentialRings.js` |
| `src/architecture/plazaGallery.js` | `src/layers/residentialRings.js` |
| `src/architecture/plazaPlan.js` | `src/architecture/bridgeUses.js`, `src/architecture/plazaGallery.js`, `src/architecture/stationSystems.js`, `src/architecture/waterCircuit.js`, `src/bases/huntLayout.js`, `src/bases/huntRoute.js`, `src/gallery/circulation.js`, `src/gallery/district.js`, `src/gallery/lakeFabric.js`, `src/gallery/playCourt.js`, `src/gallery/program.js`, `src/gallery/shaftOpenings.js`, `src/layers/domeAndFountain.js`, `src/layers/lower/engineeringKit.js`, `src/navigation/cameras.js`, `src/park/landscapeDetail.js`, `src/park/waterfront.js` |
| `src/architecture/portTender.js` | `src/layers/third/docks.js` |
| `src/architecture/readingHall.js` | `src/architecture/libraryWindow.js` |
| `src/architecture/shieldJoints.js` | `src/architecture/dockFront.js`, `src/architecture/keelGirders.js`, `src/architecture/shieldShell.js` |
| `src/architecture/shieldShell.js` | `src/layers/residentialRings.js` |
| `src/architecture/shotTools.js` | `src/main.js` |
| `src/architecture/stationSystems.js` | `src/main.js` |
| `src/architecture/waterCircuit.js` | `src/main.js` |
| `src/bases/bedroom.js` | `src/bases/rooms.js` |
| `src/bases/bedroomLink.js` | `src/bases/bedroom.js`, `src/bases/darkBaseInteriors.js`, `src/bases/rooms.js`, `src/bases/walkControls.js`, `src/main.js` |
| `src/bases/coldWalk.js` | `src/bases/walkControls.js`, `src/layers/lower/b3/coldJunction.js`, `src/layers/lower/b3/corridors.js`, `src/layers/lower/b3/crewBlocks.js`, `src/layers/lower/b3/familyRefuge.js`, `src/layers/lower/b3/innerRing.js` |
| `src/bases/darkBaseInteriors.js` | `src/bases/bedroom.js`, `src/bases/ovalAndPipe.js`, `src/bases/rooms.js`, `src/layers/lower/b3/coldJunction.js`, `src/layers/lower/b3/familyRefuge.js` |
| `src/bases/finishes.js` | `src/bases/rooms.js` |
| `src/bases/furniture.js` | `src/bases/rooms.js`, `src/layers/lower/b3/familyRefuge.js` |
| `src/bases/heroSculpts.js` | `src/bases/stationCast.js` |
| `src/bases/huntLabels.js` | `src/bases/huntLift.js`, `src/bases/huntPassage.js` |
| `src/bases/huntLayout.js` | `src/bases/huntLift.js`, `src/bases/huntPassage.js`, `src/bases/huntRoute.js`, `src/bases/huntRoute.js`, `src/bases/walkControls.js`, `src/library/serviceBays.js`, `src/main.js`, `src/navigation/cameras.js`, `src/navigation/sections.js` |
| `src/bases/huntLift.js` | `src/bases/huntRoute.js` |
| `src/bases/huntPassage.js` | `src/bases/huntRoute.js` |
| `src/bases/huntRoute.js` | `src/layers/lower/engineeringKit.js`, `src/main.js` |
| `src/bases/layout.js` | `src/architecture/stationSystems.js`, `src/bases/bedroomLink.js`, `src/bases/darkBaseInteriors.js`, `src/bases/huntLayout.js`, `src/bases/huntLift.js`, `src/bases/huntPassage.js`, `src/bases/huntRoute.js`, `src/bases/ovalAndPipe.js`, `src/bases/rooms.js`, `src/bases/views.js`, `src/bases/walkControls.js`, `src/layers/lower/b3/baseCasings.js`, `src/layers/lower/b3/baseSurroundings.js`, `src/layers/lower/b3/corridors.js`, `src/layers/lower/b3/deckConnections.js`, `src/layers/lower/engineeringKit.js`, `src/layers/lower/provisionHoist.js`, `src/layers/refugeeLayer.js`, `src/library/serviceBays.js`, `src/main.js`, `src/navigation/hotspots.js` |
| `src/bases/lightStudy.js` | `src/bases/rooms.js` |
| `src/bases/ovalAndPipe.js` | `src/bases/rooms.js`, `src/layers/lower/b3/familyRefuge.js` |
| `src/bases/panelFloor.js` | `src/bases/rooms.js`, `src/layers/lower/b3/coldJunction.js`, `src/layers/lower/b3/familyRefuge.js` |
| `src/bases/rooms.js` | `src/layers/lower/b3/darkBase.js`, `src/layers/lower/b3/ovalBase.js`, `src/layers/lower/b3/sharedEntrance.js` |
| `src/bases/serviceBay.js` | `src/bases/rooms.js` |
| `src/bases/stationCast.js` | `src/bases/rooms.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/recyclingInteriors.js`, `src/layers/lower/b3/straightCorrInteriors.js`, `src/layers/lower/b3/wildBaseInteriors.js`, `src/library/assetShowcase.js` |
| `src/bases/taisMiniature.js` | `src/bases/heroSculpts.js`, `src/gallery/district.js` |
| `src/bases/views.js` | `src/navigation/cameras.js`, `src/navigation/sections.js` |
| `src/bases/walkControls.js` | `src/ui.js` |
| `src/bases/washroomAssets.js` | `src/main.js` |
| `src/bases/washroomModels.js` | `src/bases/rooms.js`, `src/bases/washroomAssets.js` |
| `src/bases/wildWalk.js` | `src/bases/walkControls.js`, `src/main.js`, `src/navigation/cameras.js` |
| `src/cutaway.js` | `src/architecture/berthKit.js`, `src/architecture/bridgeUses.js`, `src/architecture/dockFront.js`, `src/architecture/dockGraphics.js`, `src/architecture/flightSkin.js`, `src/architecture/hullInlays.js`, `src/architecture/keelGirders.js`, `src/architecture/lawScreen.js`, `src/architecture/libraryWindow.js`, `src/architecture/plazaGallery.js`, `src/architecture/shieldShell.js`, `src/architecture/stationSystems.js`, `src/bases/bedroom.js`, `src/bases/darkBaseInteriors.js`, `src/bases/finishes.js`, `src/bases/furniture.js`, `src/bases/heroSculpts.js`, `src/bases/huntLabels.js`, `src/bases/huntLift.js`, `src/bases/huntPassage.js`, `src/bases/lightStudy.js`, `src/bases/ovalAndPipe.js`, `src/bases/panelFloor.js`, `src/bases/rooms.js`, `src/bases/serviceBay.js`, `src/bases/taisMiniature.js`, `src/bases/washroomModels.js`, `src/foliage.js`, `src/gallery/apartmentPaint.js`, `src/gallery/carpetStories.js`, `src/gallery/district.js`, `src/gallery/heroRooms.js`, `src/gallery/homeTextiles.js`, `src/gallery/interiorFinishes.js`, `src/gallery/kit.js`, `src/gallery/studioMaterials.js`, `src/layers/cargoLayer.js`, `src/layers/deckFittings.js`, `src/layers/deckRoutes.js`, `src/layers/domeAndFountain.js`, `src/layers/lower/b3/baseSurroundings.js`, `src/layers/lower/b3/basinSurface.js`, `src/layers/lower/b3/cabinLining.js`, `src/layers/lower/b3/coldHangars.js`, `src/layers/lower/b3/coldJunction.js`, `src/layers/lower/b3/corridors.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/lowerAtmosphere.js`, `src/layers/lower/b3/recyclingInteriors.js`, `src/layers/lower/b3/serviceGeometry.js`, `src/layers/lower/b3/squareWell.js`, `src/layers/lower/b3/straightCorrInteriors.js`, `src/layers/lower/b3/wildBase.js`, `src/layers/lower/b3/wildBaseInteriors.js`, `src/layers/lower/b4/distributionHall.js`, `src/layers/lower/b4/keel.js`, `src/layers/lower/b4/reactorEnvelope.js`, `src/layers/lower/passengerLanding.js`, `src/layers/refugeeLayer.js`, `src/layers/residentialRings.js`, `src/layers/utilityLayer.js`, `src/library/industrialProps.js`, `src/library/modelLibrary.js`, `src/library/plantDeck.js`, `src/library/recoveryStations.js`, `src/library/technicalPlant.js`, `src/main.js`, `src/park/landscapeDetail.js`, `src/ui.js` |
| `src/designDecisions.js` | `src/ui.js` |
| `src/foliage.js` | `src/layers/domeAndFountain.js`, `src/layers/residentialRings.js`, `src/park/landscapeDetail.js`, `src/park/waterfront.js` |
| `src/furniture/profiles.js` | `src/furniture/registry.js` |
| `src/furniture/registry.js` | `src/gallery/kit.js`, `src/gallery/sculptedFurniture.js`, `src/library/assetShowcase.js`, `src/library/assetShowcase.js` |
| `src/fx/detailLod.js` | `src/main.js` |
| `src/fx/postfx.js` | `src/main.js` |
| `src/gallery/apartmentFittings.js` | `src/gallery/heroRooms.js` |
| `src/gallery/apartmentPaint.js` | `src/gallery/heroRooms.js` |
| `src/gallery/carpetStories.js` | `src/bases/rooms.js`, `src/gallery/district.js`, `src/layers/third/nursery.js`, `src/layers/third/residential.js` |
| `src/gallery/circulation.js` | `src/architecture/plazaGallery.js`, `src/main.js` |
| `src/gallery/civic.js` | `src/gallery/district.js` |
| `src/gallery/district.js` | `src/main.js` |
| `src/gallery/efficientBevel.js` | `src/gallery/kit.js` |
| `src/gallery/flatLighting.js` | `src/gallery/district.js` |
| `src/gallery/furniture.js` | `src/gallery/civic.js`, `src/gallery/homes.js` |
| `src/gallery/heroRooms.js` | `src/gallery/district.js` |
| `src/gallery/homePlan.js` | `src/architecture/plazaGallery.js`, `src/bases/huntRoute.js`, `src/gallery/apartmentFittings.js`, `src/gallery/apartmentPaint.js`, `src/gallery/carpetStories.js`, `src/gallery/circulation.js`, `src/gallery/district.js`, `src/gallery/flatLighting.js`, `src/gallery/heroRooms.js`, `src/gallery/homeTextiles.js`, `src/gallery/homes.js`, `src/gallery/interiorFinishes.js`, `src/gallery/program.js`, `src/gallery/roomLighting.js`, `src/gallery/sculptedFurniture.js`, `src/gallery/shell.js` |
| `src/gallery/homeTextiles.js` | `src/gallery/district.js`, `src/gallery/homes.js` |
| `src/gallery/homes.js` | `src/gallery/district.js` |
| `src/gallery/interiorFinishes.js` | `src/gallery/district.js` |
| `src/gallery/interiorProbe.js` | `src/gallery/heroRooms.js`, `src/gallery/roomLighting.js`, `src/gallery/studioMaterials.js` |
| `src/gallery/kit.js` | `src/bases/huntLift.js`, `src/bases/huntPassage.js`, `src/bases/huntRoute.js`, `src/gallery/civic.js`, `src/gallery/district.js`, `src/gallery/furniture.js`, `src/gallery/homes.js`, `src/gallery/lakeFabric.js`, `src/gallery/playCourt.js`, `src/gallery/shell.js` |
| `src/gallery/lakeFabric.js` | `src/main.js`, `src/navigation/cameras.js` |
| `src/gallery/palettes.js` | `src/gallery/civic.js`, `src/gallery/homes.js`, `src/gallery/sculptedFurniture.js` |
| `src/gallery/planDialog.js` | `src/ui.js` |
| `src/gallery/playCourt.js` | `src/gallery/district.js`, `src/gallery/lakeFabric.js` |
| `src/gallery/program.js` | `src/architecture/plazaGallery.js`, `src/bases/huntRoute.js`, `src/gallery/circulation.js`, `src/gallery/district.js`, `src/gallery/interiorFinishes.js`, `src/navigation/cameras.js` |
| `src/gallery/roomLighting.js` | `src/gallery/district.js` |
| `src/gallery/sculptedFurniture.js` | `src/gallery/heroRooms.js`, `src/gallery/roomLighting.js` |
| `src/gallery/shaftOpenings.js` | `src/architecture/stationSystems.js`, `src/bases/huntLayout.js`, `src/gallery/circulation.js`, `src/gallery/district.js`, `src/layers/cargoLayer.js`, `src/layers/lower/engineeringKit.js`, `src/layers/lower/passengerLanding.js`, `src/layers/residentialRings.js`, `src/layers/utilityLayer.js` |
| `src/gallery/shell.js` | `src/gallery/district.js` |
| `src/gallery/studioMaterials.js` | `src/gallery/district.js`, `src/gallery/heroRooms.js` |
| `src/layers/cargoLayer.js` | `src/main.js` |
| `src/layers/clinicalFigures.js` | `src/layers/third/hospital.js`, `src/layers/third/nursery.js` |
| `src/layers/deckFittings.js` | `src/bases/rooms.js`, `src/layers/deckRoutes.js`, `src/layers/lower/b3/familyRefuge.js`, `src/layers/lower/b3/innerRing.js`, `src/layers/lower/b4/distributionHall.js`, `src/layers/lower/b4/machineGallery.js`, `src/layers/lower/b4/vesselFittings.js`, `src/layers/lower/engineeringKit.js`, `src/layers/lower/maintenanceAccess.js`, `src/layers/lower/passengerLanding.js`, `src/layers/lower/provisionHoist.js`, `src/layers/lower/ventAccess.js`, `src/layers/lower/wasteStairs.js`, `src/layers/lowerInteriors.js`, `src/library/placedDetails.js`, `src/library/recoveryStations.js` |
| `src/layers/deckRoutes.js` | `src/main.js`, `src/navigation/cameras.js`, `src/ui.js` |
| `src/layers/domeAndFountain.js` | `src/main.js` |
| `src/layers/levelThreeDetail.js` | `src/layers/residentialRings.js` |
| `src/layers/lower/b3/abandonedCells.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/baseCasings.js` | `src/layers/lower/b3/deckConnections.js` |
| `src/layers/lower/b3/baseSurroundings.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/basinSurface.js` | `src/layers/lower/b3/deckConnections.js` |
| `src/layers/lower/b3/cabinLining.js` | `src/layers/lower/b3/innerRing.js` |
| `src/layers/lower/b3/coldHangars.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/coldJunction.js` | `src/layers/lower/b3/deckConnections.js` |
| `src/layers/lower/b3/coreRing.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/corridors.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/crewBlocks.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/crewQuarters.js` | `src/layers/lower/b3/innerRing.js` |
| `src/layers/lower/b3/darkBase.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/deckConnections.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/familyRefuge.js` | `src/layers/lower/b3/innerRing.js` |
| `src/layers/lower/b3/hangarLabInteriors.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/industrialBays.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/innerRing.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/lowerAtmosphere.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/machineryRing.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/ovalBase.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/recycling.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/recyclingInteriors.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/repairWorkshops.js` | `src/layers/lower/b3/deckConnections.js` |
| `src/layers/lower/b3/roofProfiles.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/salvageCells.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/serviceDoors.js` | `src/layers/lower/b3/corridors.js`, `src/layers/lower/b3/deckConnections.js`, `src/layers/lower/b3/innerRing.js` |
| `src/layers/lower/b3/serviceGeometry.js` | `src/layers/lower/b3/basinSurface.js`, `src/layers/lower/b3/coldJunction.js`, `src/layers/lower/b3/deckConnections.js`, `src/layers/lower/b3/repairWorkshops.js`, `src/layers/lower/b3/serviceDoors.js`, `src/layers/lower/b3/wildWorks.js` |
| `src/layers/lower/b3/servicePlan.js` | `src/layers/lower/b3/corridors.js`, `src/layers/lower/b3/crewBlocks.js`, `src/layers/lower/b3/deckConnections.js`, `src/layers/lower/b3/innerRing.js`, `src/layers/lower/b3/machineryRing.js` |
| `src/layers/lower/b3/sharedEntrance.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/shiftRooms.js` | `src/layers/lower/b3/innerRing.js` |
| `src/layers/lower/b3/squareWell.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/straightCorrInteriors.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/wildBase.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/wildBaseInteriors.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b3/wildWorks.js` | `src/layers/lower/b3/deckConnections.js` |
| `src/layers/lower/b4/distributionHall.js` | `src/layers/lower/b4/keel.js` |
| `src/layers/lower/b4/keel.js` | `src/layers/refugeeLayer.js` |
| `src/layers/lower/b4/machineGallery.js` | `src/layers/lower/b4/keel.js` |
| `src/layers/lower/b4/reactorEnvelope.js` | `src/layers/lower/b4/keel.js`, `src/layers/refugeeLayer.js` |
| `src/layers/lower/b4/vesselFittings.js` | `src/layers/lower/b4/keel.js` |
| `src/layers/lower/engineeringKit.js` | `src/main.js` |
| `src/layers/lower/maintenanceAccess.js` | `src/layers/cargoLayer.js`, `src/layers/utilityLayer.js` |
| `src/layers/lower/passengerLanding.js` | `src/layers/lower/b3/machineryRing.js`, `src/ui.js` |
| `src/layers/lower/provisionHoist.js` | `src/bases/ovalAndPipe.js`, `src/layers/cargoLayer.js`, `src/layers/lowerInteriors.js`, `src/navigation/cameras.js` |
| `src/layers/lower/reactorRisers.js` | `src/layers/lower/b3/coreRing.js`, `src/layers/lower/b4/keel.js` |
| `src/layers/lower/ventAccess.js` | `src/layers/utilityLayer.js` |
| `src/layers/lower/wasteStairs.js` | `src/layers/cargoLayer.js`, `src/layers/lowerInteriors.js` |
| `src/layers/lowerInteriors.js` | `src/main.js`, `src/navigation/cameras.js`, `src/navigation/sections.js`, `src/ui.js` |
| `src/layers/medicalInteriors.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/nurseryEquipment.js` | `src/layers/medicalInteriors.js` |
| `src/layers/refugeeLayer.js` | `src/main.js` |
| `src/layers/residentialRings.js` | `src/main.js` |
| `src/layers/space.js` | `src/main.js` |
| `src/layers/third/bridge.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/circulation.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/docks.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/filterBay.js` | `src/layers/third/lifeSupport.js` |
| `src/layers/third/hospital.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/lifeSupport.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/nursery.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/residential.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/robotics.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/third/warehouses.js` | `src/layers/levelThreeDetail.js` |
| `src/layers/utilityLayer.js` | `src/main.js` |
| `src/library/assetKit.js` | `src/bases/rooms.js`, `src/layers/cargoLayer.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/recyclingInteriors.js`, `src/layers/lower/b3/straightCorrInteriors.js`, `src/layers/lower/b3/wildBaseInteriors.js`, `src/layers/residentialRings.js`, `src/library/assetShowcase.js`, `src/library/industrialProps.js` |
| `src/library/assetShowcase.js` | `src/main.js` |
| `src/library/b4Distribution.js` | `src/layers/lower/b4/distributionHall.js`, `src/main.js`, `src/navigation/cameras.js`, `src/navigation/sections.js` |
| `src/library/coldSites.js` | `src/library/serviceBays.js` |
| `src/library/hangarDeckLayout.js` | `src/library/hangarFloor.js` |
| `src/library/hangarDocks.js` | `src/layers/lower/b3/coldHangars.js`, `src/layers/refugeeLayer.js`, `src/library/hangarEnvelope.js`, `src/library/hangarFloor.js`, `src/library/hangarFreight.js`, `src/library/hangarHandling.js` |
| `src/library/hangarEnvelope.js` | `src/layers/lower/b3/coldHangars.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/library/hangarFreight.js` |
| `src/library/hangarFloor.js` | `src/library/hangarFreight.js` |
| `src/library/hangarFreight.js` | `src/library/coldSites.js` |
| `src/library/hangarHandling.js` | `src/library/hangarFloor.js`, `src/library/hangarFreight.js` |
| `src/library/hangarShots.js` | `src/navigation/cameras.js`, `src/ui.js` |
| `src/library/hangarSteelPlates.js` | `src/layers/levelThreeDetail.js`, `src/layers/lower/b3/coldHangars.js` |
| `src/library/hangarStores.js` | `src/library/coldSites.js`, `src/library/hangarFreight.js` |
| `src/library/industrialProps.js` | `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/recyclingInteriors.js`, `src/library/assetShowcase.js` |
| `src/library/modelFiles.js` | `src/bases/washroomAssets.js`, `src/library/modelLibrary.js`, `src/main.js` |
| `src/library/modelInspector.js` | `src/main.js` |
| `src/library/modelLibrary.js` | `src/bases/rooms.js`, `src/bases/stationCast.js`, `src/layers/deckFittings.js`, `src/layers/lower/b3/coldHangars.js`, `src/layers/lower/b3/coldJunction.js`, `src/layers/lower/b3/familyRefuge.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/recyclingInteriors.js`, `src/layers/lower/b3/squareWell.js`, `src/layers/lower/b3/straightCorrInteriors.js`, `src/layers/lower/b3/wildBaseInteriors.js`, `src/layers/lower/b4/keel.js`, `src/layers/lower/b4/reactorEnvelope.js`, `src/layers/lower/passengerLanding.js`, `src/layers/lower/provisionHoist.js`, `src/layers/third/filterBay.js`, `src/library/modelInspector.js`, `src/library/placedDetails.js`, `src/library/serviceBays.js`, `src/library/technicalPlant.js`, `src/main.js` |
| `src/library/modelUrls.js` | `src/library/modelFiles.js` |
| `src/library/placedDetails.js` | `src/bases/ovalAndPipe.js`, `src/gallery/district.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/wildBaseInteriors.js`, `src/main.js` |
| `src/library/plantDeck.js` | `src/library/technicalPlant.js` |
| `src/library/recoveryStations.js` | `src/layers/lower/b3/recyclingInteriors.js`, `src/layers/refugeeLayer.js`, `src/library/serviceBays.js` |
| `src/library/serviceBays.js` | `src/layers/lower/b3/serviceDoors.js`, `src/layers/lowerInteriors.js`, `src/main.js` |
| `src/library/technicalPlant.js` | `src/layers/refugeeLayer.js` |
| `src/main.js` | Точка входу |
| `src/navigation/cameras.js` | `src/navigation/navigator.js`, `src/ui.js` |
| `src/navigation/guidedVisit.js` | `src/navigation/navigator.js` |
| `src/navigation/hotspots.js` | `src/ui.js` |
| `src/navigation/navigator.js` | `src/main.js` |
| `src/navigation/sections.js` | `src/ui.js` |
| `src/park/botanicalTextures.js` | `src/foliage.js` |
| `src/park/flowers.js` | `src/park/landscapeDetail.js` |
| `src/park/landscapeDetail.js` | `src/layers/domeAndFountain.js` |
| `src/park/waterfront.js` | `src/layers/domeAndFountain.js`, `src/park/landscapeDetail.js` |
| `src/people.js` | `src/architecture/plazaGallery.js`, `src/layers/domeAndFountain.js`, `src/layers/refugeeLayer.js`, `src/layers/residentialRings.js` |
| `src/scale.js` | `src/architecture/bridgeUses.js`, `src/architecture/flightSkin.js`, `src/architecture/lawScreen.js`, `src/architecture/plazaGallery.js`, `src/architecture/plazaPlan.js`, `src/architecture/readingHall.js`, `src/architecture/stationSystems.js`, `src/bases/bedroom.js`, `src/bases/coldWalk.js`, `src/bases/darkBaseInteriors.js`, `src/bases/finishes.js`, `src/bases/furniture.js`, `src/bases/huntLayout.js`, `src/bases/huntLift.js`, `src/bases/huntPassage.js`, `src/bases/huntRoute.js`, `src/bases/layout.js`, `src/bases/lightStudy.js`, `src/bases/ovalAndPipe.js`, `src/bases/panelFloor.js`, `src/bases/rooms.js`, `src/bases/stationCast.js`, `src/bases/washroomModels.js`, `src/bases/wildWalk.js`, `src/gallery/circulation.js`, `src/gallery/district.js`, `src/gallery/lakeFabric.js`, `src/gallery/playCourt.js`, `src/gallery/program.js`, `src/gallery/shaftOpenings.js`, `src/layers/deckFittings.js`, `src/layers/domeAndFountain.js`, `src/layers/levelThreeDetail.js`, `src/layers/lower/b3/baseSurroundings.js`, `src/layers/lower/b3/cabinLining.js`, `src/layers/lower/b3/coldHangars.js`, `src/layers/lower/b3/familyRefuge.js`, `src/layers/lower/b3/hangarLabInteriors.js`, `src/layers/lower/b3/recyclingInteriors.js`, `src/layers/lower/b3/straightCorrInteriors.js`, `src/layers/lower/b3/wildBase.js`, `src/layers/lower/b3/wildBaseInteriors.js`, `src/layers/lower/b4/distributionHall.js`, `src/layers/lower/b4/machineGallery.js`, `src/layers/lower/b4/vesselFittings.js`, `src/layers/lower/engineeringKit.js`, `src/layers/lower/maintenanceAccess.js`, `src/layers/lower/passengerLanding.js`, `src/layers/lower/provisionHoist.js`, `src/layers/lower/ventAccess.js`, `src/layers/lower/wasteStairs.js`, `src/layers/third/filterBay.js`, `src/library/assetShowcase.js`, `src/library/hangarDocks.js`, `src/library/hangarEnvelope.js`, `src/library/hangarFloor.js`, `src/library/hangarFreight.js`, `src/library/hangarShots.js`, `src/library/industrialProps.js`, `src/library/modelLibrary.js`, `src/library/placedDetails.js`, `src/library/recoveryStations.js`, `src/library/serviceBays.js`, `src/library/technicalPlant.js`, `src/park/waterfront.js`, `src/ui.js` |
| `src/stationTiers.js` | `src/main.js` |
| `src/textures.js` | `src/architecture/lawScreen.js`, `src/layers/cargoLayer.js`, `src/layers/domeAndFountain.js`, `src/layers/refugeeLayer.js`, `src/layers/residentialRings.js`, `src/layers/utilityLayer.js` |
| `src/thirdDeckMap.js` | `src/navigation/cameras.js`, `src/ui.js` |
| `src/ui.js` | `src/main.js` |

## Камери кімнат нижнього рівня

| ID | Палуба | Кімната |
|---|---|---|
| `wasteStairs` | B3 | Відчинені двері до сміттєвого цеху |
| `lonLanding` | B3 | Ліфт Лона · повернення з другого рівня |
| `coldFork` | B3 | Три проходи за воротами колодязя |
| `lostCabin` | B3 | Покинуті каюти за воротами |
| `familyRefuge` | B3 | Пізнє укриття Овальних · у гостях із Колею |
| `shiftWash` | B3 | Вмивальня зміни біля Ангару 2 |
| `shiftWatch` | B3 | Кімната вахти біля Ангару 2 |
| `sorting` | B3 | Сортувальний пост |
| `recoveryPack` | B3 | Оборотна тара · вихід із преса |
| `recoveryBio` | B3 | Органіка · розвантаження барабана |
| `waterService` | B3 | Майданчик водяних насосів |
| `repairBench` | B3 | Верстак ремонту Донів |
| `wildMess` | B3 | Стіл Диких |
| `recoveryParts` | B3 | Знахідки в залізному ящику |
| `bayToolCrib` | B3 | Інструментальна комора |
| `bayCableTrench` | B3 | Кабельна траншея |
| `bayBackupPower` | B3 | Акумуляторна резервного живлення |
| `bayHydraulicBench` | B3 | Гідравлічна насосна |
| `bayDonService` | B3 | Пост діагностики Донів |
| `bayAirPlant` | B3 | Пневматична ресиверна |
| `bayGarage` | B3 | Гараж візків · Ангар 2 |
| `bayArchive` | B3 | Холодний архів Професора |
| `bayOvalGallery` | B3 | Вимірювальна галерея · вихід Овальної |
| `bayCrewOne` | B3 | Роздягальня · Ангар 1 |
| `bayCrewTwo` | B3 | Роздягальня · Ангар 2 |
| `bayCrewThree` | B3 | Роздягальня · Ангар 3 |
| `bayScrap` | B3 | Приймання вторсировини |
| `bayGreywater` | B3 | Зворотна вода · за душовою |
| `trussStairs` | B1 | Сходова вежа під фермою |
| `ventFoot` | B1 | Сервісний вхід у вентиляційну шахту |
| `filterBench` | B1 | Сервісна касета |
| `receiving` | B2 | Пост приймання |
| `ovalSupplyHead` | B2 | Верхня станція кошика Овальних |
| `ballastValve` | B2 | Пост баластного колектора |
| `bankGallery` | B4 | Галерея накопичувачів |
| `vesselLanding` | B4 | Майданчик ревізії ємності |
| `heatService` | B4 | Вузол теплового контуру |
| `ashService` | B4 | Приймання золи |
| `basesDistrict` | B3 | Сектор баз · оточення B3 |
| `darkPlan` | B3 | Темна база · план усіх кімнат |
| `youngRoom` | B3 | Спальня молодших |
| `farRoom` | B3 | Дальня спальня |
| `darkoval` | B3 | Темна база · спільна кімната |
| `taisFigure` | B3 | Таїс · Темна база |
| `sharedDoor` | B3 | Спільні двері та розвилка |
| `basePipe` | B3 | Круглий лаз |
| `bedroomEye` | B3 | Спальня · з висоти очей |
| `springBed` | B3 | Спальня Таїс і Федора |
| `sleepLanding` | B3 | Спальня · підйом від спільної кімнати |
| `baseServices` | B3 | Вода та повітря · сервісна шафа |
| `darkWash` | B3 | Душова та бойлер |
| `darkBunks` | B3 | Спальні Темної бази |
| `memorial` | B3 | Стіна пам’яті |
| `stores` | B3 | Комори зі стелажами |
| `ovalbase` | B3 | Овальна база · загальний вигляд |
| `ovalAccess` | B3 | Овальна · шахта B2 і запасний хід |
| `ovalBeds` | B3 | Чотири ліжка та тумбочки |
| `ovalTea` | B3 | Стіл Овальних |
