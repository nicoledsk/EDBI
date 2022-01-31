SELECT *
FROM [PortfolioProject ]..CovidDeaths$
order by 3,4

SELECT *
FROM [PortfolioProject ]..CovidVaccinations$
order by 3,4

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM [PortfolioProject ]..CovidDeaths$
ORDER BY 1,2 

-- looking at total cases vs total deaths 
-- Shows likelihood of dying if you contract covid in your country (UK)

SELECT location, date, total_cases, total_deaths,(total_deaths/total_cases)*100 AS DeathPercentage
FROM [PortfolioProject ]..CovidDeaths$
-- WHERE location like '%Kingdom%' 
ORDER BY 1,2 

-- Looking at total cases vs population
-- Shows what percentage of population got covid (UK)

SELECT location, date, total_cases, population,(total_deaths/population)*100 AS DeathPercentage
FROM [PortfolioProject ]..CovidDeaths$
-- WHERE location like '%Kingdom%'
ORDER BY 1,2

-- Looking at countries with highest infection rates compared to population

SELECT location, MAX(total_cases) AS HighestInfectionCount, population,MAX((total_cases/population))*100 AS PercentPopInfected
FROM [PortfolioProject ]..CovidDeaths$
GROUP BY location, population
ORDER BY PercentPopInfected desc

-- 22.6% of UK infected with Covid to date (reported figures - could be greater)
-- Next : Showing countries with highest death count per population 

SELECT location, MAX(cast(total_deaths as int)) AS TotalDeathCount
FROM [PortfolioProject ]..CovidDeaths$
WHERE continent is not null
GROUP BY location
ORDER BY totaldeathcount desc

-- Analyse by continent 
-- Total death count 

SELECT continent, MAX(cast(total_deaths as int)) AS TotalDeathCount
FROM [PortfolioProject ]..CovidDeaths$
WHERE continent is not null
GROUP BY continent
ORDER BY totaldeathcount desc

--Global numbers

SELECT date, SUM(new_cases) as total_cases, SUM(cast (new_deaths as int)) as total_deaths, SUM(cast (new_deaths as int))/SUM(new_cases)*100 AS GlobalDeathPercent
FROM [PortfolioProject ]..CovidDeaths$
WHERE continent is not null
GROUP BY date
ORDER BY 1,2

-- Total population vs Vaccinations 
-- Showing percentage of population that has has at least one vaccine 

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) as RollingPplVaccinated
--, (Rollingpplvacinated/population)*100
FROM [PortfolioProject ]..CovidDeaths$ dea
JOIN  [PortfolioProject ]..CovidVaccinations$ vac 
 ON dea.location = vac.location
AND dea.date = vac.date
WHERE dea.continent is not null
--ORDER BY 2,3

--Temp Table
DROP table if exists #PercentPopulationVaccinated 
Create table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
Rollingpplvaccinated numeric
)

Insert into #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) as RollingPplVaccinated
--, (Rollingpplvacinated/population)*100
FROM [PortfolioProject ]..CovidDeaths$ dea
JOIN  [PortfolioProject ]..CovidVaccinations$ vac 
 ON dea.location = vac.location
AND dea.date = vac.date
WHERE dea.continent is not null
--AND dea.location like '%Kingdom%'
--ORDER BY 2,3

SELECT *, (Rollingpplvaccinated/population)*100
FROM #PercentPopulationVaccinated

-- USE CTE 

With PopvsVac (continent, location, date, population, new_vaccinations, Rollingpplvaccinated)
as 
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) as RollingPplVaccinated
--, (Rollingpplvacinated/population)*100
FROM [PortfolioProject ]..CovidDeaths$ dea
JOIN  [PortfolioProject ]..CovidVaccinations$ vac 
 ON dea.location = vac.location
AND dea.date = vac.date
WHERE dea.continent is not null
--AND dea.location like '%Kingdom%'
--ORDER BY 2,3
)
SELECT *, (Rollingpplvaccinated/population)*100
FROM PopvsVac

-- To note results are counting single vaccinations. Individuals who recieve second or booster are counted as additional persons. Percentage will exceed 100

-- Creating view to store data later for visualisations 

Create view PercentPopVaxed as
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) as RollingPplVaccinated
--, (Rollingpplvacinated/population)*100
FROM [PortfolioProject ]..CovidDeaths$ dea
JOIN  [PortfolioProject ]..CovidVaccinations$ vac 
 ON dea.location = vac.location
AND dea.date = vac.date
WHERE dea.continent is not null
--AND dea.location like '%Kingdom%'
--ORDER BY 2,3
