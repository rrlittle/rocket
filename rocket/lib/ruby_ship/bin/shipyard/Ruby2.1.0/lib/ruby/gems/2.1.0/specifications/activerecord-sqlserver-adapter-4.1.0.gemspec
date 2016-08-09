# -*- encoding: utf-8 -*-
# stub: activerecord-sqlserver-adapter 4.1.0 ruby lib

Gem::Specification.new do |s|
  s.name = "activerecord-sqlserver-adapter"
  s.version = "4.1.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib"]
  s.authors = ["Ken Collins", "Anna Carey", "Will Bond", "Murray Steele", "Shawn Balestracci", "Joe Rafaniello", "Tom Ward"]
  s.date = "2014-05-23"
  s.description = "ActiveRecord SQL Server Adapter. For SQL Server 2005 And Higher."
  s.email = "ken@metaskills.net"
  s.homepage = "http://github.com/rails-sqlserver/activerecord-sqlserver-adapter"
  s.rubyforge_project = "activerecord-sqlserver-adapter"
  s.rubygems_version = "2.2.2"
  s.summary = "ActiveRecord SQL Server Adapter. For SQL Server 2005 And Higher."

  s.installed_by_version = "2.2.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<activerecord>, ["~> 4.1.0"])
      s.add_runtime_dependency(%q<arel>, [">= 0"])
    else
      s.add_dependency(%q<activerecord>, ["~> 4.1.0"])
      s.add_dependency(%q<arel>, [">= 0"])
    end
  else
    s.add_dependency(%q<activerecord>, ["~> 4.1.0"])
    s.add_dependency(%q<arel>, [">= 0"])
  end
end
