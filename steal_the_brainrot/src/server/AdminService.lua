local AdminService = {}

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Configuration
local GameConfig = require(ReplicatedStorage.GameConfig)

function AdminService.IsAdmin(player)
	if type(player) == "number" then
		return GameConfig.ADMIN_IDS[player] or false
	elseif typeof(player) == "Instance" and player:IsA("Player") then
		return GameConfig.ADMIN_IDS[player.UserId] or false
	end
	return false
end

function AdminService.CreateAdminRoom()
	local room = Instance.new("Part")
	room.Name = "AdminRoom"
	room.Size = Vector3.new(50, 1, 50)
	room.Position = Vector3.new(0, 1000, 0)
	room.Anchored = true
	room.BrickColor = BrickColor.new("Really black")
	room.Material = Enum.Material.Neon
	room.Parent = workspace

	-- Add walls (Secure box)
	local wallHeight = 10
	local wallThickness = 1
	local walls = {
		{Size = Vector3.new(50, wallHeight, wallThickness), Pos = Vector3.new(0, wallHeight/2, 25)},
		{Size = Vector3.new(50, wallHeight, wallThickness), Pos = Vector3.new(0, wallHeight/2, -25)},
		{Size = Vector3.new(wallThickness, wallHeight, 50), Pos = Vector3.new(25, wallHeight/2, 0)},
		{Size = Vector3.new(wallThickness, wallHeight, 50), Pos = Vector3.new(-25, wallHeight/2, 0)},
	}

	for _, w in ipairs(walls) do
		local wall = Instance.new("Part")
		wall.Size = w.Size
		wall.Position = room.Position + w.Pos
		wall.Anchored = true
		wall.BrickColor = BrickColor.new("Really black")
		wall.Material = Enum.Material.Metal
		wall.Transparency = 0.5
		wall.Parent = room
	end

	-- Ceiling
	local ceiling = Instance.new("Part")
	ceiling.Size = room.Size
	ceiling.Position = room.Position + Vector3.new(0, wallHeight, 0)
	ceiling.Anchored = true
	ceiling.BrickColor = BrickColor.new("Really black")
	ceiling.Material = Enum.Material.Neon
	ceiling.Parent = room

	return room
end

function AdminService.SpawnTheThinker(position)
	local thinker = Instance.new("Part")
	thinker.Name = "TheThinker"
	thinker.Size = Vector3.new(4, 8, 4)
	if position then
		thinker.Position = position
	else
		-- Default spawn near origin if no pos
		thinker.Position = Vector3.new(0, 10, 0)
	end
	thinker.Anchored = true
	thinker.BrickColor = BrickColor.new("Bronze")
	thinker.Material = Enum.Material.Metal

	-- Add a label
	local bb = Instance.new("BillboardGui")
	bb.Size = UDim2.new(0, 100, 0, 50)
	bb.Adornee = thinker
	bb.AlwaysOnTop = true
	bb.Parent = thinker

	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1,0,1,0)
	lbl.Text = "The Thinker"
	lbl.BackgroundTransparency = 1
	lbl.TextColor3 = Color3.new(1,1,1)
	lbl.Parent = bb

	thinker.Parent = workspace
	return thinker
end

function AdminService.KickAll(reason)
	for _, player in ipairs(Players:GetPlayers()) do
		if not AdminService.IsAdmin(player) then
			player:Kick(reason or "Admin initiated kick all.")
		end
	end
end

function AdminService.ResetMap()
	local map = workspace:FindFirstChild("Map")
	if map then
		map:Destroy()
	end

	-- Assuming WorldGenerator is available via some global or re-require
	-- For simplicity, we might need to rely on the GameManager to trigger this
	-- or re-require the WorldGenerator script if it's a module.
	-- Since WorldGenerator is a .server.lua (Script), it runs once.
	-- Ideally WorldGenerator should be a ModuleScript required by a main script.
	-- I'll address this by assuming we can signal the game manager.
end

return AdminService
