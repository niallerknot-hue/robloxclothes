local WorldGenerator = {}

-- Services
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Modules
local AssetConfig = require(ReplicatedStorage.AssetConfig)

local MAP_SIZE = 200
local PART_COUNT = 50

function WorldGenerator.Generate()
	-- Create a folder for the map
	local mapFolder = Instance.new("Folder")
	mapFolder.Name = "Map"
	mapFolder.Parent = workspace

	-- Create Baseplate
	local baseplate = Instance.new("Part")
	baseplate.Name = "Baseplate"
	baseplate.Size = Vector3.new(MAP_SIZE, 1, MAP_SIZE)
	baseplate.Position = Vector3.new(0, 0, 0)
	baseplate.Anchored = true
	baseplate.BrickColor = BrickColor.new("Dark green")
	baseplate.Material = Enum.Material.Grass
	baseplate.Parent = mapFolder

	-- Generate Random Parts
	for i = 1, PART_COUNT do
		local part = Instance.new("Part")
		part.Size = Vector3.new(math.random(5, 15), math.random(5, 20), math.random(5, 15))
		part.Position = Vector3.new(
			math.random(-MAP_SIZE/2, MAP_SIZE/2),
			part.Size.Y / 2,
			math.random(-MAP_SIZE/2, MAP_SIZE/2)
		)
		part.Anchored = true
		part.BrickColor = BrickColor.Random()
		part.Material = Enum.Material.Plastic -- Could vary this
		part.Parent = mapFolder
	end

	-- Generate Landmarks from AssetConfig
	for _, landmark in ipairs(AssetConfig.Landmarks) do
		local zone = Instance.new("Part")
		zone.Name = landmark.Name
		zone.Size = Vector3.new(20, 10, 20)
		-- Find a random spot not too close to center
		local x = math.random(-MAP_SIZE/2 + 20, MAP_SIZE/2 - 20)
		local z = math.random(-MAP_SIZE/2 + 20, MAP_SIZE/2 - 20)
		zone.Position = Vector3.new(x, 5, z)
		zone.Color = landmark.Color
		zone.Material = landmark.Material
		zone.Anchored = true
		zone.Parent = mapFolder

		-- Add Label
		local surfaceGui = Instance.new("SurfaceGui")
		surfaceGui.Face = Enum.NormalId.Top
		surfaceGui.Parent = zone

		local textLabel = Instance.new("TextLabel")
		textLabel.Size = UDim2.new(1, 0, 1, 0)
		textLabel.BackgroundTransparency = 1
		textLabel.Text = landmark.Name
		textLabel.TextScaled = true
		textLabel.Parent = surfaceGui
	end
end

return WorldGenerator
