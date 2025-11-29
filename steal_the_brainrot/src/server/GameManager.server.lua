local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local RunService = game:GetService("RunService")

local AdminService = require(script.Parent.AdminService)
local AssetConfig = require(ReplicatedStorage.AssetConfig)
-- Since WorldGenerator is now a ModuleScript in src/server (ServerScriptService), we can require it.
-- Rojo maps src/server to ServerScriptService.
local WorldGenerator = require(ServerScriptService.WorldGenerator)

-- Initial Map Generation
WorldGenerator.Generate()

-- Game State
local currentHolder = nil
local brainrotItem = nil

-- Create Leaderstats
local function onPlayerAdded(player)
	local leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	leaderstats.Parent = player

	local points = Instance.new("IntValue")
	points.Name = "BrainrotPoints"
	points.Value = 0
	points.Parent = leaderstats
end

Players.PlayerAdded:Connect(onPlayerAdded)

-- Brainrot Item Logic
local function spawnBrainrot()
	if brainrotItem then brainrotItem:Destroy() end

	brainrotItem = Instance.new("Part")
	brainrotItem.Name = "Brainrot"
	brainrotItem.Size = Vector3.new(2, 2, 2)
	brainrotItem.Position = Vector3.new(0, 10, 0)
	brainrotItem.BrickColor = BrickColor.new("Electric blue")
	brainrotItem.Material = Enum.Material.Neon
	brainrotItem.Shape = Enum.PartType.Ball
	brainrotItem.Parent = workspace

	-- Stealing Mechanic
	brainrotItem.Touched:Connect(function(hit)
		local character = hit.Parent
		local player = Players:GetPlayerFromCharacter(character)

		if player and player ~= currentHolder then
			-- Transfer item
			currentHolder = player

			-- Visual feedback
			brainrotItem.BrickColor = BrickColor.new("Really red")

			-- Attach to player (weld)
			local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
			if humanoidRootPart then
				brainrotItem.CFrame = humanoidRootPart.CFrame * CFrame.new(0, 3, 0)

				local weld = Instance.new("WeldConstraint")
				weld.Part0 = humanoidRootPart
				weld.Part1 = brainrotItem
				weld.Parent = brainrotItem
				brainrotItem.Anchored = false
				brainrotItem.CanCollide = false
			end

			print(player.Name .. " stole the Brainrot!")
		end
	end)
end

spawnBrainrot()

-- Scoring Loop
task.spawn(function()
	while true do
		task.wait(1)
		if currentHolder and currentHolder.Parent then -- check if player still in game
			local stats = currentHolder:FindFirstChild("leaderstats")
			if stats then
				local points = stats:FindFirstChild("BrainrotPoints")
				if points then
					points.Value = points.Value + 1
				end
			end
		else
			currentHolder = nil
			-- If holder left or died, maybe respawn item?
			if not brainrotItem or not brainrotItem.Parent then
				spawnBrainrot()
			elseif brainrotItem.Parent and brainrotItem.Parent:IsA("Model") then
				-- attached to character
				-- Detach if character is gone/dead handled by physics usually but we want to be sure
			end
		end
	end
end)


-- Handle Admin Remote Events
-- Create Remotes if they don't exist
local Remotes = ReplicatedStorage:FindFirstChild("Remotes")
if not Remotes then
	Remotes = Instance.new("Folder")
	Remotes.Name = "Remotes"
	Remotes.Parent = ReplicatedStorage
end

local AdminEvent = Remotes:FindFirstChild("AdminEvent")
if not AdminEvent then
	AdminEvent = Instance.new("RemoteEvent")
	AdminEvent.Name = "AdminEvent"
	AdminEvent.Parent = Remotes
end

AdminEvent.OnServerEvent:Connect(function(player, action, ...)
	if not AdminService.IsAdmin(player) then
		warn(player.Name .. " attempted to use admin command " .. tostring(action))
		return
	end

	if action == "TeleportAdmin" then
		local char = player.Character
		if char and char:FindFirstChild("HumanoidRootPart") then
			char.HumanoidRootPart.CFrame = CFrame.new(0, 1005, 0)
		end
		AdminService.CreateAdminRoom() -- Ensure room exists

	elseif action == "KickAll" then
		AdminService.KickAll()

	elseif action == "SpawnThinker" then
		local char = player.Character
		local pos = char and char.PrimaryPart and char.PrimaryPart.Position
		AdminService.SpawnTheThinker(pos and pos + Vector3.new(5,0,0))

	elseif action == "ResetMap" then
		AdminService.ResetMap()
		-- Regenerate map
		WorldGenerator.Generate()
		print("Map reset and regenerated.")
	end
end)
