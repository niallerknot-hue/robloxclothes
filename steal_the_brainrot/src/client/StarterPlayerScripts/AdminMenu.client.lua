local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player = Players.LocalPlayer
local PlayerGui = player:WaitForChild("PlayerGui")

local GameConfig = require(ReplicatedStorage.GameConfig)

-- Check if Admin (Client-side check only for UI visibility, server verifies actions)
local function isAdmin(p)
	return GameConfig.ADMIN_IDS[p.UserId] or false
end

if not isAdmin(player) then
	return -- Do nothing if not admin
end

-- Create UI
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "AdminMenu"
screenGui.ResetOnSpawn = false
screenGui.Parent = PlayerGui

local frame = Instance.new("Frame")
frame.Name = "MainFrame"
frame.Size = UDim2.new(0, 200, 0, 300)
frame.Position = UDim2.new(0, 10, 0.5, -150)
frame.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
frame.BorderSizePixel = 0
frame.Parent = screenGui

local title = Instance.new("TextLabel")
title.Text = "Admin Panel"
title.Size = UDim2.new(1, 0, 0, 40)
title.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
title.TextColor3 = Color3.new(1, 1, 1)
title.Font = Enum.Font.SourceSansBold
title.TextSize = 18
title.Parent = frame

local layout = Instance.new("UIListLayout")
layout.Padding = UDim.new(0, 5)
layout.FillDirection = Enum.FillDirection.Vertical
layout.HorizontalAlignment = Enum.HorizontalAlignment.Center
layout.SortOrder = Enum.SortOrder.LayoutOrder
layout.Parent = frame

-- Padding for title
local p = Instance.new("UIPadding")
p.PaddingTop = UDim.new(0, 45) -- Push buttons down
p.Parent = frame

local function createButton(text, action)
	local btn = Instance.new("TextButton")
	btn.Size = UDim2.new(0.9, 0, 0, 40)
	btn.BackgroundColor3 = Color3.fromRGB(80, 80, 80)
	btn.Text = text
	btn.TextColor3 = Color3.new(1, 1, 1)
	btn.Font = Enum.Font.SourceSans
	btn.TextSize = 14
	btn.Parent = frame

	btn.MouseButton1Click:Connect(function()
		local Remotes = ReplicatedStorage:WaitForChild("Remotes")
		local AdminEvent = Remotes:WaitForChild("AdminEvent")
		AdminEvent:FireServer(action)
	end)
end

createButton("Teleport to Admin Room", "TeleportAdmin")
createButton("Kick All", "KickAll")
createButton("Spawn The Thinker", "SpawnThinker")
createButton("Reset Map", "ResetMap")
