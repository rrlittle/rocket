# -*- encoding: utf-8 -*-
# stub: dicom 0.9.6 ruby lib

Gem::Specification.new do |s|
  s.name = "dicom"
  s.version = "0.9.6"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib"]
  s.authors = ["Christoffer Lervag"]
  s.date = "2014-06-20"
  s.description = "DICOM is a standard widely used throughout the world to store and transfer medical image data. This library enables efficient and powerful handling of DICOM in Ruby, to the benefit of any student or professional who would like to use their favorite language to process DICOM files and communicate across the network."
  s.email = "chris.lervag@gmail.com"
  s.homepage = "http://dicom.rubyforge.org/"
  s.licenses = ["GPLv3"]
  s.required_ruby_version = Gem::Requirement.new(">= 1.9.3")
  s.rubyforge_project = "dicom"
  s.rubygems_version = "2.2.2"
  s.summary = "Library for handling DICOM files and DICOM network communication."

  s.installed_by_version = "2.2.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<bundler>, ["~> 1.6"])
      s.add_development_dependency(%q<mini_magick>, ["~> 3.7"])
      s.add_development_dependency(%q<mocha>, ["~> 1.1"])
      s.add_development_dependency(%q<narray>, [">= 0.6.0.8", "~> 0.6"])
      s.add_development_dependency(%q<rake>, ["~> 10.3"])
      s.add_development_dependency(%q<redcarpet>, ["~> 3.1"])
      s.add_development_dependency(%q<rmagick>, [">= 2.13.2", "~> 2.13"])
      s.add_development_dependency(%q<rspec>, ["~> 3.0"])
      s.add_development_dependency(%q<yard>, [">= 0.8.7", "~> 0.8"])
    else
      s.add_dependency(%q<bundler>, ["~> 1.6"])
      s.add_dependency(%q<mini_magick>, ["~> 3.7"])
      s.add_dependency(%q<mocha>, ["~> 1.1"])
      s.add_dependency(%q<narray>, [">= 0.6.0.8", "~> 0.6"])
      s.add_dependency(%q<rake>, ["~> 10.3"])
      s.add_dependency(%q<redcarpet>, ["~> 3.1"])
      s.add_dependency(%q<rmagick>, [">= 2.13.2", "~> 2.13"])
      s.add_dependency(%q<rspec>, ["~> 3.0"])
      s.add_dependency(%q<yard>, [">= 0.8.7", "~> 0.8"])
    end
  else
    s.add_dependency(%q<bundler>, ["~> 1.6"])
    s.add_dependency(%q<mini_magick>, ["~> 3.7"])
    s.add_dependency(%q<mocha>, ["~> 1.1"])
    s.add_dependency(%q<narray>, [">= 0.6.0.8", "~> 0.6"])
    s.add_dependency(%q<rake>, ["~> 10.3"])
    s.add_dependency(%q<redcarpet>, ["~> 3.1"])
    s.add_dependency(%q<rmagick>, [">= 2.13.2", "~> 2.13"])
    s.add_dependency(%q<rspec>, ["~> 3.0"])
    s.add_dependency(%q<yard>, [">= 0.8.7", "~> 0.8"])
  end
end
