# 部署指南

### System模块部署方法
1. 需要site模块支持与配置
2. 添加`system`到installed apps
3. 添加MIDDLEWARE, `system.middleware.site.CurrentSiteMiddleware`
4. 添加TEMPLATES中`context_processors`, `system.context_processors.site_info`